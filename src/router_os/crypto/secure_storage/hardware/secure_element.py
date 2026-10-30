"""Secure Element provider interface."""


class SecureElementProvider:
    available = False

    def initialize(self) -> None:
        return None

    def store_non_exportable(self, key_id: str, material: bytes) -> None:
        raise NotImplementedError("Secure Element backend is platform-specific")

    def load_non_exportable(self, key_id: str) -> bytes:
        raise NotImplementedError("Secure Element backend is platform-specific")
