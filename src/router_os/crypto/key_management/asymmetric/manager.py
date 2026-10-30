"""Asymmetric identity key manager."""
from ..key_manager import KeyManager


class AsymmetricKeyManager:
    def __init__(self, manager: KeyManager | None = None) -> None:
        self.manager = manager or KeyManager()

    def ensure_identity(self):
        return self.manager.ensure_asymmetric_identity()
