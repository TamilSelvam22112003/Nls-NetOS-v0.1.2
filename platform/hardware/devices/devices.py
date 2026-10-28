"""Hardware device abstraction and Linux sysfs inventory."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

SYSFS = Path("/sys")


@dataclass(frozen=True)
class Device:
    """Stable description of a host device discovered from sysfs."""

    name: str
    subsystem: str
    sysfs_path: str
    driver: str | None = None
    properties: dict[str, str] = field(default_factory=dict)

    @property
    def bound(self) -> bool:
        return self.driver is not None


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def _driver(path: Path) -> str | None:
    link = path / "driver"
    try:
        return link.resolve().name if link.exists() else None
    except OSError:
        return None


def list_block_devices() -> list[str]:
    root = SYSFS / "class/block"
    return [p.name for p in sorted(root.iterdir())] if root.exists() else []


def list_platform_devices() -> list[str]:
    root = SYSFS / "bus/platform/devices"
    return [p.name for p in sorted(root.iterdir())] if root.exists() else []


def list_network_devices() -> list[str]:
    root = SYSFS / "class/net"
    return [p.name for p in sorted(root.iterdir())] if root.exists() else []


def describe_network_device(name: str) -> Device | None:
    path = SYSFS / "class/net" / name
    if not path.exists():
        return None
    properties = {
        key: value
        for key in ("address", "operstate", "mtu", "ifindex")
        if (value := _read(path / key)) is not None
    }
    return Device(
        name=name,
        subsystem="net",
        sysfs_path=str(path),
        driver=_driver(path),
        properties=properties,
    )


def describe_block_device(name: str) -> Device | None:
    path = SYSFS / "class/block" / name
    if not path.exists():
        return None
    properties = {
        key: value
        for key in ("dev", "size", "ro", "removable")
        if (value := _read(path / key)) is not None
    }
    return Device(
        name=name,
        subsystem="block",
        sysfs_path=str(path),
        driver=_driver(path),
        properties=properties,
    )


def inventory() -> list[Device]:
    """Return discoverable network and block devices."""
    devices: list[Device] = []
    for name in list_network_devices():
        if device := describe_network_device(name):
            devices.append(device)
    for name in list_block_devices():
        if device := describe_block_device(name):
            devices.append(device)
    return devices
