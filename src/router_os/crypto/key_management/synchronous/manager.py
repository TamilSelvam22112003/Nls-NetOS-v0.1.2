"""Synchronous key manager."""
from ..key_manager import KeyManager


class SynchronousKeyManager:
    def __init__(self, manager: KeyManager | None = None) -> None:
        self.manager = manager or KeyManager()

    def ensure(self):
        return self.manager.ensure_synchronous()
