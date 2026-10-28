"""Portable platform discovery for Linux-based router appliances."""

from __future__ import annotations

import os
import platform
from pathlib import Path
from typing import Any, Dict, List


_SYSFS = Path("/sys")


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8").strip() or None
    except (OSError, UnicodeError):
        return None


def _list_names(path: Path) -> List[str]:
    try:
        return sorted(p.name for p in path.iterdir())
    except OSError:
        return []


def discover_platform() -> Dict[str, Any]:
    """Return hardware/OS facts without changing system state."""
    interfaces = _list_names(_SYSFS / "class" / "net")
    pci_devices = _list_names(_SYSFS / "bus" / "pci" / "devices")

    return {
        "os": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "cpu_count": os.cpu_count() or 1,
        "interfaces": interfaces,
        "pci_devices": pci_devices,
        "virtualized": _read_text(_SYSFS / "class" / "dmi" / "id" / "product_name"),
    }


__all__ = ["discover_platform"]
