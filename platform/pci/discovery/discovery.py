"""PCI bus discovery through Linux sysfs."""
from pathlib import Path

ROOT = Path("/sys/bus/pci/devices")


def list_devices():
    return [p.name for p in sorted(ROOT.iterdir())] if ROOT.exists() else []


def attribute(bdf, name):
    try:
        return (ROOT / bdf / name).read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None
