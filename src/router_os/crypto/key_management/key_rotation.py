"""Explicit key rotation operations."""
from __future__ import annotations
from .key_version import next_version
from .key_generator import KeyGenerator
from ..secure_storage.secure_store import SecureStore, StoredKey


class KeyRotation:
    def __init__(self, store: SecureStore | None = None) -> None:
        self.store = store or SecureStore()

    def rotate_synchronous(self) -> StoredKey:
        old = self.store.get("nls-synchronous")
        version = next_version(old.version if old else 0)
        new = StoredKey("nls-synchronous", "symmetric", version, secret=KeyGenerator.synchronous_key())
        self.store.put(new)
        return new
