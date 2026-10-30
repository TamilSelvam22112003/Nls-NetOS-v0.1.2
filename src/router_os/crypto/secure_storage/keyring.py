"""Keyring-style facade over SecureStore."""
from .secure_store import SecureStore


class Keyring:
    def __init__(self, store: SecureStore | None = None):
        self.store = store or SecureStore()

    def get(self, key_id: str):
        return self.store.get(key_id)

    def put(self, key):
        self.store.put(key)
