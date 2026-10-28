"""DPDK backend discovery and execution planning for Ubuntu.

The planner never binds or unbinds a NIC implicitly. It produces an explicit
plan after hardware detection so deployment tooling can require operator
approval before changing host networking.
"""

from __future__ import annotations

from dataclasses import dataclass
import shutil
from pathlib import Path
import subprocess

from .hardware_probe import NICInfo, recommend_backend


@dataclass(frozen=True)
class DPDKEnvironment:
    installed: bool
    version: str | None
    devbind: str | None
    vfio_pci: bool
    uio_pci_generic: bool
    hugepages: int


@dataclass(frozen=True)
class BindingPlan:
    interface: str
    pci_address: str
    current_driver: str | None
    target_driver: str | None
    pmd: str | None
    backend: str
    safe_to_bind: bool
    reason: str


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except OSError:
        return None


def environment() -> DPDKEnvironment:
    dpdk = shutil.which("dpdk-testpmd") or shutil.which("dpdk-pdump")
    devbind = shutil.which("dpdk-devbind.py")
    if devbind is None:
        for candidate in (
            "/usr/share/dpdk/usertools/dpdk-devbind.py",
            "/usr/bin/dpdk-devbind.py",
        ):
            if Path(candidate).exists():
                devbind = candidate
                break
    version = None
    if dpdk:
        try:
            output = subprocess.run([dpdk, "--version"], capture_output=True, text=True, timeout=2)
            version = (output.stdout or output.stderr).strip().splitlines()[0] if output.returncode == 0 else None
        except (OSError, subprocess.SubprocessError):
            pass
    return DPDKEnvironment(
        installed=dpdk is not None,
        version=version,
        devbind=devbind,
        vfio_pci=Path("/sys/bus/pci/drivers/vfio-pci").exists(),
        uio_pci_generic=Path("/sys/bus/pci/drivers/uio_pci_generic").exists(),
        hugepages=sum(
            int(v) for p in Path("/sys/kernel/mm/hugepages").glob("hugepages-*/nr_hugepages")
            if (v := _read(p) or "0").isdigit()
        ) if Path("/sys/kernel/mm/hugepages").exists() else 0,
    )


def plan(nic: NICInfo, env: DPDKEnvironment | None = None) -> BindingPlan:
    env = env or environment()
    recommendation = recommend_backend(nic)
    if recommendation.backend.startswith("dpdk") or recommendation.backend == "dpdk":
        target = "vfio-pci" if env.vfio_pci else ("uio_pci_generic" if env.uio_pci_generic else None)
        safe = bool(env.installed and nic.pci_address and target)
        reason = (
            "DPDK and a userspace PCI binding driver are available; operator approval is still required."
            if safe
            else "DPDK, VFIO/UIO, or required host prerequisites are missing."
        )
        return BindingPlan(nic.interface, nic.pci_address or "", nic.kernel_driver, target, recommendation.pmd, recommendation.backend, safe, reason)
    return BindingPlan(nic.interface, nic.pci_address or "", nic.kernel_driver, nic.kernel_driver, None, recommendation.backend, False, recommendation.reason)


def plans(nics: list[NICInfo]) -> list[BindingPlan]:
    env = environment()
    return [plan(nic, env) for nic in nics]
