"""NIC lifecycle abstraction backed by Linux sysfs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class NIC:
    name: str
    driver: str | None = None
    running: bool = False
    attached: bool = False

    def attach(self, driver: str | None = None) -> None:
        discovered = driver or discover_driver(self.name)
        self.driver = discovered
        self.attached = True
        self.running = True

    def detach(self) -> None:
        self.running = False
        self.attached = False

    def refresh(self) -> bool:
        root = Path("/sys/class/net") / self.name
        if not root.exists():
            self.running = False
            self.attached = False
            return False
        state = _read(root / "operstate")
        self.running = state == "up"
        self.driver = discover_driver(self.name)
        self.attached = True
        return True


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def discover_driver(name: str) -> str | None:
    root = Path("/sys/class/net") / name / "device/driver"
    try:
        return root.resolve().name if root.exists() else None
    except OSError:
        return None


def discover() -> list[NIC]:
    root = Path("/sys/class/net")
    if not root.exists():
        return []
    nics = []
    for path in sorted(root.iterdir()):
        nic = NIC(path.name)
        nic.refresh()
        nics.append(nic)
    return nics
