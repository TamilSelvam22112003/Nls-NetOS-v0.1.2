"""CPU topology discovery."""
from pathlib import Path
import os

CPU_ROOT = Path("/sys/devices/system/cpu")


def logical_cpus():
    return os.cpu_count() or 1


def online_cpus():
    path = CPU_ROOT / "online"
    try:
        return path.read_text().strip()
    except OSError:
        return None


def cpu_ids():
    return sorted(int(p.name[3:]) for p in CPU_ROOT.glob("cpu[0-9]*") if p.name[3:].isdigit())
