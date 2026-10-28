"""SR-IOV capability and virtual-function controls for PCI devices."""

from __future__ import annotations

from pathlib import Path

PCI = Path("/sys/bus/pci/devices")


def _path(bdf: str, name: str) -> Path:
    return PCI / bdf / name


def capabilities(bdf: str) -> dict[str, int | bool]:
    root = PCI / bdf
    if not root.exists():
        raise FileNotFoundError(root)
    total = _read_int(root / "sriov_totalvfs")
    current = _read_int(root / "sriov_numvfs")
    return {
        "supported": total is not None,
        "total_vfs": total or 0,
        "enabled_vfs": current or 0,
    }


def _read_int(path: Path) -> int | None:
    try:
        return int(path.read_text().strip())
    except (OSError, ValueError):
        return None


def enable_vfs(bdf: str, count: int) -> None:
    if count < 0:
        raise ValueError("count must be non-negative")
    total = _read_int(_path(bdf, "sriov_totalvfs"))
    if total is None:
        raise RuntimeError(f"PCI device {bdf} does not expose SR-IOV")
    if count > total:
        raise ValueError(f"count exceeds sriov_totalvfs ({total})")
    _path(bdf, "sriov_numvfs").write_text(str(count))


def disable_vfs(bdf: str) -> None:
    enable_vfs(bdf, 0)
