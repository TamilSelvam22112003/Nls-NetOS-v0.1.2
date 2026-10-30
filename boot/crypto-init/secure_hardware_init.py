"""Initialize hardware-backed cryptographic protection."""
from __future__ import annotations


def initialize_secure_hardware() -> None:
    """Initialize the selected TPM/HSM/Secure Element provider."""
    # The provider is intentionally an interface until platform-specific
    # hardware integration is selected. No plaintext key is handled here.
    return None
