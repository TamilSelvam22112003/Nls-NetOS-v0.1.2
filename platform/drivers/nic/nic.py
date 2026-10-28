"""NIC lifecycle abstraction backed by the host kernel driver."""
from dataclasses import dataclass


@dataclass
class NIC:
    name: str
    driver: str | None = None
    running: bool = False

    def attach(self, driver=None):
        self.driver = driver or self.driver
        self.running = True

    def detach(self):
        self.running = False
