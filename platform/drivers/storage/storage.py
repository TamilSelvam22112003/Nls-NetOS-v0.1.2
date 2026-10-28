"""Storage device abstraction and Linux block-device discovery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SYSFS = Path("/sys")


@dataclass(frozen=True)
class StorageDevice:
    name: str
    path: str
    removable: bool = False
    size_bytes: int = 0
    read_only: bool = False


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def device(name: str, path: str | None = None, removable: bool = False) -> StorageDevice:
    root = SYSFS / "class/block" / name
    size_sectors = int(_read(root / "size") or 0)
    detected_removable = (_read(root / "removable") == "1")
    read_only = (_read(root / "ro") == "1")
    return StorageDevice(
        name=name,
        path=path or f"/dev/{name}",
        removable=removable or detected_removable,
        size_bytes=size_sectors * 512,
        read_only=read_only,
    )


def discover() -> list[StorageDevice]:
    root = SYSFS / "class/block"
    if not root.exists():
        return []
    return [device(path.name) for path in sorted(root.iterdir())]
