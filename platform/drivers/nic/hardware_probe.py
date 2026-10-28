"""Ubuntu/Linux NIC inventory and backend selection.

This module deliberately discovers hardware before selecting a dataplane backend.
It never unbinds a NIC or changes host networking state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import os
import platform
import re
import subprocess

PCI_ROOT = Path("/sys/bus/pci/devices")
NET_ROOT = Path("/sys/class/net")


@dataclass(frozen=True)
class NICInfo:
    interface: str
    pci_address: str | None
    vendor_id: str | None
    device_id: str | None
    subsystem_vendor: str | None
    subsystem_device: str | None
    pci_class: str | None
    kernel_driver: str | None
    link_speed_mbps: int | None
    mac: str | None
    mtu: int | None
    state: str | None
    iommu_group: str | None
    sriov_total_vfs: int
    sriov_num_vfs: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BackendRecommendation:
    backend: str
    pmd: str | None
    reason: str
    requires_vfio: bool
    requires_dpdk: bool
    confidence: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def _int(path: Path, default: int = 0) -> int:
    value = _read(path)
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


def _pci_for_interface(interface: str) -> Path | None:
    device = NET_ROOT / interface / "device"
    try:
        resolved = device.resolve()
    except OSError:
        return None
    return resolved if resolved.exists() else None


def _speed(interface: str) -> int | None:
    value = _read(NET_ROOT / interface / "speed")
    try:
        return int(value) if value is not None and int(value) >= 0 else None
    except ValueError:
        return None


def _driver(pci: Path) -> str | None:
    try:
        return (pci / "driver").resolve().name
    except OSError:
        return None


def _iommu_group(pci: Path) -> str | None:
    try:
        return (pci / "iommu_group").resolve().name
    except OSError:
        return None


def inventory() -> list[NICInfo]:
    """Return physical/virtual Ethernet interfaces backed by PCI devices."""
    result: list[NICInfo] = []
    if not NET_ROOT.exists():
        return result
    for netdev in sorted(NET_ROOT.iterdir(), key=lambda p: p.name):
        if netdev.name == "lo":
            continue
        pci = _pci_for_interface(netdev.name)
        if pci is None:
            continue
        result.append(
            NICInfo(
                interface=netdev.name,
                pci_address=pci.name,
                vendor_id=_read(pci / "vendor"),
                device_id=_read(pci / "device"),
                subsystem_vendor=_read(pci / "subsystem_vendor"),
                subsystem_device=_read(pci / "subsystem_device"),
                pci_class=_read(pci / "class"),
                kernel_driver=_driver(pci),
                link_speed_mbps=_speed(netdev.name),
                mac=_read(netdev / "address"),
                mtu=_int(netdev / "mtu", 1500),
                state=_read(netdev / "operstate"),
                iommu_group=_iommu_group(pci),
                sriov_total_vfs=_int(pci / "sriov_totalvfs"),
                sriov_num_vfs=_int(pci / "sriov_numvfs"),
            )
        )
    return result


def ubuntu_details() -> dict[str, str | None]:
    """Return deployment-relevant Ubuntu/kernel/CPU information."""
    os_release: dict[str, str] = {}
    try:
        for line in Path("/etc/os-release").read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                os_release[key] = value.strip().strip('"')
    except OSError:
        pass
    return {
        "distribution": os_release.get("PRETTY_NAME"),
        "version_id": os_release.get("VERSION_ID"),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "cpu_count": str(os.cpu_count() or 1),
    }


def _dpdk_bind_available() -> bool:
    return any(
        Path(candidate).exists()
        for candidate in (
            "/usr/bin/dpdk-devbind.py",
            "/usr/share/dpdk/usertools/dpdk-devbind.py",
        )
    )


def _dpdk_driver_available(name: str) -> bool:
    return Path(f"/sys/bus/pci/drivers/{name}").exists()


def recommend_backend(nic: NICInfo) -> BackendRecommendation:
    """Select the safest available backend for a discovered NIC.

    PMD selection is intentionally conservative. A vendor PMD is selected only
    from a known PCI vendor/device family; otherwise Linux kernel networking is
    retained rather than guessing.
    """
    vendor = (nic.vendor_id or "").lower()
    device = (nic.device_id or "").lower()
    driver = (nic.kernel_driver or "").lower()

    # Intel Ethernet families commonly used with ixgbe/ice/i40e/idpf.
    if vendor == "0x8086":
        if driver == "ice" or device in {"0x1592", "0x1593", "0x1889", "0x188a"}:
            return _dpdk("ice", "Intel Ethernet device is compatible with the DPDK ICE PMD.")
        if driver == "i40e":
            return _dpdk("i40e", "Kernel driver identifies an Intel i40e device.")
        if driver == "ixgbe":
            return _dpdk("ixgbe", "Kernel driver identifies an Intel ixgbe device.")
        if driver in {"igb", "igc"}:
            return _dpdk(driver, f"Kernel driver identifies Intel {driver}; verify PMD support for the exact device.")
        return _dpdk("unknown-intel", "Intel NIC detected; exact PMD must be validated against the PCI device ID.", confidence="medium")

    # NVIDIA/Mellanox ConnectX family uses mlx5 PMD and normally remains
    # attached to mlx5_core in the Linux bifurcated-driver model.
    if vendor in {"0x15b3", "0x1f67"} or driver == "mlx5_core":
        return BackendRecommendation(
            backend="dpdk-mlx5",
            pmd="mlx5",
            reason="NVIDIA/Mellanox NIC detected; DPDK mlx5 supports the ConnectX/BlueField family.",
            requires_vfio=False,
            requires_dpdk=True,
            confidence="high",
        )

    if driver == "virtio-pci":
        return BackendRecommendation("dpdk-virtio", "virtio", "Virtio PCI NIC detected.", False, True, "high")

    if _dpdk_bind_available() and nic.pci_address:
        return BackendRecommendation("dpdk-generic", None, "DPDK tooling is installed but no safe vendor PMD mapping was identified.", True, True, "low")

    return BackendRecommendation("linux-kernel", None, "No validated DPDK PMD mapping was identified; retain the Linux kernel driver.", False, False, "high")


def _dpdk(pmd: str, reason: str, confidence: str = "high") -> BackendRecommendation:
    return BackendRecommendation("dpdk", pmd, reason, not _dpdk_driver_available("vfio-pci"), True, confidence)


def inspect() -> dict[str, object]:
    nics = inventory()
    return {
        "ubuntu": ubuntu_details(),
        "nics": [nic.as_dict() for nic in nics],
        "backends": {nic.interface: recommend_backend(nic).as_dict() for nic in nics},
    }
