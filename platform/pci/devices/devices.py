"""PCI device inventory and identity helpers."""
from pathlib import Path

ROOT = Path("/sys/bus/pci/devices")


def devices():
    return [p.name for p in sorted(ROOT.iterdir())] if ROOT.exists() else []


def identity(bdf):
    result = {"bdf": bdf}
    for name in ("vendor", "device", "subsystem_vendor", "subsystem_device", "class"):
        try:
            result[name] = (ROOT / bdf / name).read_text().strip()
        except OSError:
            result[name] = None
    return result
