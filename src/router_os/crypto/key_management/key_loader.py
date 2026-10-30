"""Load NLS keys through the secure-storage boundary."""
from __future__ import annotations
from ..secure_storage.secure_store import SecureStore, StoredKey


class KeyLoader:
    def __init__(self, store: SecureStore | None = None) -> None:
        self.store = store or SecureStore()

    def load(self, key_id: str) -> StoredKey | None:
        return self.store.get(key_id)
