"""Linux NIC IRQ, RPS and XPS helpers.

Writes are explicit and opt-in; discovery functions are read-only.
"""

from __future__ import annotations

from pathlib import Path

NET = Path("/sys/class/net")


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def irq_affinity(interface: str) -> dict[str, str]:
    """Return per-queue RPS/XPS masks exposed by sysfs."""
    root = NET / interface / "queues"
    if not root.exists():
        return {}
    result: dict[str, str] = {}
    for queue in sorted(root.iterdir()):
        for key in ("rps_cpus", "xps_cpus"):
            value = _read(queue / key)
            if value is not None:
                result[f"{queue.name}/{key}"] = value
    return result


def set_queue_mask(interface: str, queue: str, mask: str, direction: str) -> None:
    """Set an RPS/XPS CPU mask; caller must have appropriate privileges."""
    if direction not in {"rps", "xps"}:
        raise ValueError("direction must be 'rps' or 'xps'")
    if not mask or any(ch not in "0123456789abcdefABCDEF," for ch in mask):
        raise ValueError("mask must be a Linux hexadecimal CPU mask")
    path = NET / interface / "queues" / queue / f"{direction}_cpus"
    if not path.exists():
        raise FileNotFoundError(path)
    path.write_text(mask)
