"""High-level NLS key lifecycle manager."""
from __future__ import annotations

from .key_generator import KeyGenerator
from .key_lifecycle import KeyLifecycle
from ..secure_storage.secure_store import SecureStore, StoredKey


class KeyManager:
    def __init__(self, store: SecureStore | None = None) -> None:
        self.store = store or SecureStore()
        self.generator = KeyGenerator()

    def ensure_synchronous(self) -> StoredKey:
        current = self.store.get("nls-synchronous")
        if current:
            return current
        key = StoredKey("nls-synchronous", "symmetric", 1, secret=self.generator.synchronous_key())
        self.store.put(key)
        return key

    def ensure_asymmetric_identity(self) -> StoredKey:
        current = self.store.get("nls-identity")
        if current:
            return current
        private, public = self.generator.asymmetric_keypair()
        key = StoredKey("nls-identity", "ed25519", 1, public_key=public, secret=private)
        self.store.put(key)
        return key

    def lifecycle(self, key: StoredKey) -> KeyLifecycle:
        return KeyLifecycle(key_id=key.key_id, version=key.version)
