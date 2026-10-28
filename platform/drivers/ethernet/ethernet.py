"""Ethernet port model and kernel-backed interface operations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EthernetPort:
    name: str
    mac: str | None = None
    mtu: int | None = None
    state: str | None = None
    driver: str | None = None


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def port(name: str, mac: str | None = None, mtu: int | None = None) -> EthernetPort:
    if not name:
        raise ValueError("interface name must not be empty")
    return EthernetPort(name=name, mac=mac, mtu=mtu)


def inspect(name: str) -> EthernetPort | None:
    root = Path("/sys/class/net") / name
    if not root.exists():
        return None
    driver = None
    try:
        link = root / "device/driver"
        if link.exists():
            driver = link.resolve().name
    except OSError:
        pass
    return EthernetPort(
        name=name,
        mac=_read(root / "address"),
        mtu=int(_read(root / "mtu") or 0) or None,
        state=_read(root / "operstate"),
        driver=driver,
    )


def list_ports() -> list[EthernetPort]:
    root = Path("/sys/class/net")
    if not root.exists():
        return []
    return [item for name in sorted(p.name for p in root.iterdir()) if (item := inspect(name))]
