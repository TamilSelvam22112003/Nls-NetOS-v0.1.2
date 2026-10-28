"""Capability detection for the platform layer."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict


def _exists(path: str) -> bool:
    return Path(path).exists()


def detect_capabilities(discovery: Dict[str, Any]) -> Dict[str, Any]:
    """Derive safe, runtime-neutral capabilities from discovered facts."""
    return {
        "cpu": {
            "logical_cpus": int(discovery.get("cpu_count") or (os.cpu_count() or 1)),
            "numa_sysfs": _exists("/sys/devices/system/node"),
        },
        "memory": {
            "hugepages_sysfs": _exists("/sys/kernel/mm/hugepages"),
        },
        "network": {
            "sysfs": _exists("/sys/class/net"),
            "interface_count": len(discovery.get("interfaces", [])),
        },
        "pci": {
            "sysfs": _exists("/sys/bus/pci"),
            "device_count": len(discovery.get("pci_devices", [])),
        },
        "platform": {
            "linux": discovery.get("os") == "Linux",
            "architecture": discovery.get("architecture"),
        },
    }


__all__ = ["detect_capabilities"]
