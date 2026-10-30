"""TPM secure-storage provider interface."""


class TPMProvider:
    available = False

    def initialize(self) -> None:
        """Probe and initialize the platform TPM integration."""
        return None

    def store_non_exportable(self, key_id: str, material: bytes) -> None:
        raise NotImplementedError("TPM backend is platform-specific")

    def load_non_exportable(self, key_id: str) -> bytes:
        raise NotImplementedError("TPM backend is platform-specific")
