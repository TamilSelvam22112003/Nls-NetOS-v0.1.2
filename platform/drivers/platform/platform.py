"""Generic platform-driver lifecycle abstraction."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlatformDriver:
    name: str
    resources: dict[str, Any] = field(default_factory=dict)
    started: bool = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False
