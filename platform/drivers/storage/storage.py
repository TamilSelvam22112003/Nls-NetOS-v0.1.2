"""Storage device abstraction for router services."""
from dataclasses import dataclass


@dataclass(frozen=True)
class StorageDevice:
    name: str
    path: str
    removable: bool = False


def device(name, path, removable=False):
    return StorageDevice(name, path, removable)
