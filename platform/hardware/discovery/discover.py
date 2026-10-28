"""Hardware discovery helpers for Linux router platforms."""
from pathlib import Path

SYSFS = Path("/sys")


def discover_devices():
    """Return basic devices visible through Linux sysfs."""
    devices = []
    root = SYSFS / "class"
    if root.exists():
        for cls in sorted(root.iterdir()):
            try:
                devices.extend(str(p) for p in sorted(cls.iterdir()))
            except OSError:
                continue
    return devices


def discover_network_interfaces():
    """Return network interfaces exposed by Linux."""
    root = SYSFS / "class/net"
    return [p.name for p in sorted(root.iterdir())] if root.exists() else []
