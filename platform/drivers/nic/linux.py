"""Linux NIC backend for discovery and safe queue/affinity inspection."""

from __future__ import annotations

from pathlib import Path


NET = Path("/sys/class/net")


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def driver(name: str) -> str | None:
    path = NET / name / "device/driver"
    try:
        return path.resolve().name if path.exists() else None
    except OSError:
        return None


def channels(name: str) -> dict[str, int]:
    """Read ethtool channel counts when exported by the driver."""
    root = NET / name / "device"
    result: dict[str, int] = {}
    # Kernel sysfs does not expose a universal ethtool channel ABI; return
    # queue counts where standard queue directories are available.
    for kind in ("rx", "tx"):
        queue_root = NET / name / "queues"
        prefix = f"{kind}-"
        if queue_root.exists():
            count = len([p for p in queue_root.iterdir() if p.name.startswith(prefix)])
            if count:
                result[kind] = count
    return result


def queue_affinity(name: str) -> dict[str, str]:
    root = NET / name / "queues"
    if not root.exists():
        return {}
    result: dict[str, str] = {}
    for queue in sorted(root.iterdir()):
        mask = _read(queue / "rps_cpus") or _read(queue / "xps_cpus")
        if mask is not None:
            result[queue.name] = mask
    return result
