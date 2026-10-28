"""Portable CPU affinity helpers."""
import os


def available_cpus():
    try:
        return sorted(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return list(range(os.cpu_count() or 1))


def set_process_affinity(cpus):
    """Set affinity for the current process; raises on unsupported systems."""
    os.sched_setaffinity(0, set(cpus))
