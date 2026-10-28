"""Intel-focused DPDK packet-engine launcher and validation.

The packet engine is intentionally implemented as a native DPDK application
boundary. NetOS does not reimplement Intel NIC register programming: Intel's
DPDK PMD performs device-specific MMIO, descriptor and DMA operations.

This module validates the host and launches an operator-approved DPDK binary.
It does not automatically bind/unbind PCI devices or steal the host's NIC.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess

from .dpdk_backend import DPDKEnvironment, environment
from .hardware_probe import NICInfo, recommend_backend


@dataclass(frozen=True)
class EngineReadiness:
    ready: bool
    interface: str
    pci_address: str
    pmd: str | None
    dpdk_installed: bool
    vfio_available: bool
    hugepages: int
    reason: str


def _is_intel(nic: NICInfo) -> bool:
    return (nic.vendor_id or "").lower() == "0x8086"


def validate(nic: NICInfo, env: DPDKEnvironment | None = None) -> EngineReadiness:
    env = env or environment()
    recommendation = recommend_backend(nic)
    if not _is_intel(nic):
        return EngineReadiness(False, nic.interface, nic.pci_address or "", recommendation.pmd,
                               env.installed, env.vfio_pci, env.hugepages,
                               "This engine is restricted to Intel PCI NICs.")
    if not nic.pci_address:
        return EngineReadiness(False, nic.interface, "", recommendation.pmd,
                               env.installed, env.vfio_pci, env.hugepages,
                               "Intel NIC has no PCI address.")
    if not env.installed:
        return EngineReadiness(False, nic.interface, nic.pci_address, recommendation.pmd,
                               False, env.vfio_pci, env.hugepages,
                               "DPDK runtime is not installed.")
    if recommendation.pmd is None or recommendation.backend == "linux-kernel":
        return EngineReadiness(False, nic.interface, nic.pci_address, recommendation.pmd,
                               True, env.vfio_pci, env.hugepages,
                               "No validated Intel DPDK PMD was identified for this NIC.")
    if not env.vfio_pci:
        return EngineReadiness(False, nic.interface, nic.pci_address, recommendation.pmd,
                               True, False, env.hugepages,
                               "vfio-pci is unavailable; configure VFIO before userspace PCI access.")
    if env.hugepages < 1:
        return EngineReadiness(False, nic.interface, nic.pci_address, recommendation.pmd,
                               True, True, 0,
                               "No configured hugepages were detected.")
    return EngineReadiness(True, nic.interface, nic.pci_address, recommendation.pmd,
                           True, True, env.hugepages,
                           "Intel DPDK PMD environment is ready for an operator-approved launch.")


def command(binary: str, pci_address: str, cores: str = "0-1") -> list[str]:
    """Build an explicit DPDK EAL command without executing it."""
    if not binary or not pci_address:
        raise ValueError("binary and pci_address are required")
    return [binary, "-l", cores, "-a", pci_address]


def launch(binary: str, pci_address: str, cores: str = "0-1") -> subprocess.Popen[str]:
    """Launch a native DPDK application after explicit caller approval.

    Binding must already have been performed by deployment tooling. This
    function only starts the supplied executable with the requested PCI device.
    """
    if shutil.which(binary) is None and not Path(binary).exists():
        raise FileNotFoundError(binary)
    if os.geteuid() != 0:
        raise PermissionError("DPDK PCI datapaths normally require root or appropriate VFIO permissions")
    return subprocess.Popen(command(binary, pci_address, cores), text=True)
