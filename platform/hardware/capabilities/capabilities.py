"""Linux hardware capability detection."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import os

SYSFS = Path("/sys")


@dataclass(frozen=True)
class HardwareCapabilities:
    sysfs: bool
    hugepages: bool
    numa: bool
    iommu: bool
    sriov: bool
    xdp: bool
    af_xdp: bool
    bpf: bool
    virtualization: bool
    hotplug: bool

    def as_dict(self) -> dict[str, bool]:
        return asdict(self)


def has_sysfs() -> bool:
    return SYSFS.is_dir()


def supports_hugepages() -> bool:
    return (SYSFS / "kernel/mm/hugepages").is_dir()


def supports_numa() -> bool:
    return (SYSFS / "devices/system/node").is_dir()


def supports_iommu() -> bool:
    root = SYSFS / "class/iommu"
    if root.is_dir() and any(root.iterdir()):
        return True
    return any((SYSFS / name).exists() for name in ("class/iommu", "kernel/iommu_groups"))


def supports_sriov() -> bool:
    root = SYSFS / "bus/pci/devices"
    if not root.is_dir():
        return False
    return any((device / "sriov_totalvfs").exists() for device in root.iterdir())


def supports_bpf() -> bool:
    return Path("/sys/fs/bpf").is_dir() or Path("/proc/sys/kernel/unprivileged_bpf_disabled").exists()


def supports_xdp() -> bool:
    # XDP is a kernel networking facility. Presence of BPF support is the
    # portable capability signal; individual NICs may still lack native XDP.
    return supports_bpf()


def supports_af_xdp() -> bool:
    return supports_xdp() and hasattr(os, "AF_XDP")


def supports_virtualization() -> bool:
    return Path("/sys/hypervisor").exists() or Path("/dev/kvm").exists()


def supports_hotplug() -> bool:
    return (SYSFS / "bus/pci/rescan").exists()


def detect() -> HardwareCapabilities:
    return HardwareCapabilities(
        sysfs=has_sysfs(),
        hugepages=supports_hugepages(),
        numa=supports_numa(),
        iommu=supports_iommu(),
        sriov=supports_sriov(),
        xdp=supports_xdp(),
        af_xdp=supports_af_xdp(),
        bpf=supports_bpf(),
        virtualization=supports_virtualization(),
        hotplug=supports_hotplug(),
    )
