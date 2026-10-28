"""NUMA topology inspection without requiring privileged operations."""
from pathlib import Path

ROOT = Path("/sys/devices/system/node")


def available_nodes():
    if not ROOT.exists():
        return []
    return sorted(int(p.name[4:]) for p in ROOT.glob("node[0-9]*") if p.name[4:].isdigit())


def node_cpulist(node):
    path = ROOT / f"node{node}" / "cpulist"
    try:
        return path.read_text().strip()
    except OSError:
        return None
