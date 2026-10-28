"""PCI capability and resource inspection."""
from pathlib import Path

ROOT = Path("/sys/bus/pci/devices")


def resource_available(bdf):
    return (ROOT / bdf / "resource").exists()


def driver(bdf):
    link = ROOT / bdf / "driver"
    try:
        return link.resolve().name
    except OSError:
        return None
