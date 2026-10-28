"""PCI capability, resource, driver and SR-IOV inspection."""

from __future__ import annotations

from pathlib import Path

ROOT = Path("/sys/bus/pci/devices")


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def resource_available(bdf: str) -> bool:
    return (ROOT / bdf / "resource").exists()


def driver(bdf: str) -> str | None:
    link = ROOT / bdf / "driver"
    try:
        return link.resolve().name if link.exists() else None
    except OSError:
        return None


def device_info(bdf: str) -> dict[str, str | int | bool | None]:
    root = ROOT / bdf
    if not root.exists():
        raise FileNotFoundError(root)
    values: dict[str, str | int | bool | None] = {
        "bdf": bdf,
        "vendor": _read(root / "vendor"),
        "device": _read(root / "device"),
        "class": _read(root / "class"),
        "driver": driver(bdf),
        "resource_available": resource_available(bdf),
    }
    total = _read(root / "sriov_totalvfs")
    current = _read(root / "sriov_numvfs")
    values["sriov_total_vfs"] = int(total) if total and total.isdigit() else 0
    values["sriov_enabled_vfs"] = int(current) if current and current.isdigit() else 0
    return values
