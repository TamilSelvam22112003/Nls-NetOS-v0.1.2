"""Hardware capability probes."""
from pathlib import Path


def has_sysfs():
    return Path("/sys").is_dir()


def supports_hugepages():
    return Path("/sys/kernel/mm/hugepages").is_dir()


def supports_numa():
    return Path("/sys/devices/system/node").is_dir()
