"""Hugepage discovery and status helpers."""
from pathlib import Path

ROOT = Path("/sys/kernel/mm/hugepages")


def supported_sizes():
    if not ROOT.exists():
        return []
    return sorted(p.name for p in ROOT.glob("hugepages-*"))


def status(size_dir):
    path = ROOT / size_dir
    result = {}
    for name in ("nr_hugepages", "free_hugepages", "resv_hugepages"):
        try:
            result[name] = int((path / name).read_text().strip())
        except (OSError, ValueError):
            result[name] = None
    return result
