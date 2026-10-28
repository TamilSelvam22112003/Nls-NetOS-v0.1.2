"""Generic Linux device inventory."""
from pathlib import Path


SYSFS = Path("/sys")


def list_block_devices():
    root = SYSFS / "class/block"
    return [p.name for p in sorted(root.iterdir())] if root.exists() else []


def list_platform_devices():
    root = SYSFS / "bus/platform/devices"
    return [p.name for p in sorted(root.iterdir())] if root.exists() else []
