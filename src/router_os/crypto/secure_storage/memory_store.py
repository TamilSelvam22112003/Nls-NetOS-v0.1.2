"""Volatile secure-store implementation for tests."""
from __future__ import annotations
from .secure_store import StoredKey


class MemoryStore:
    def __init__(self):
        self._keys: dict[str, StoredKey] = {}

    def get(self, key_id: str):
        return self._keys.get(key_id)

    def put(self, key: StoredKey):
        self._keys[key.key_id] = key
