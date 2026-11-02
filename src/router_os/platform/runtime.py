from __future__ import annotations

import platform as py_platform
import socket
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PlatformSnapshot:
    operating_system: str
    kernel: str
    architecture: str
    hostname: str
    interfaces: tuple[str, ...]


class PlatformSubsystem:
    def __init__(self) -> None:
        self.snapshot: PlatformSnapshot | None = None

    def initialize(self) -> PlatformSnapshot:
        path = Path("/sys/class/net")
        interfaces = tuple(sorted(p.name for p in path.iterdir() if p.is_dir())) if path.is_dir() else ()
        self.snapshot = PlatformSnapshot(py_platform.system(), py_platform.release(), py_platform.machine(), socket.gethostname(), interfaces)
        return self.snapshot

    def start(self) -> None:
        if self.snapshot is None:
            raise RuntimeError("platform subsystem must be initialized before start")

    def stop(self) -> None:
        self.snapshot = None
