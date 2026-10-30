"""NLS cryptographic subsystem boot initialization."""

from __future__ import annotations


def initialize_crypto() -> None:
    """Initialize secure crypto hardware/storage and NLS key lifecycle."""
    from key_store_init import initialize_key_store
    from secure_hardware_init import initialize_secure_hardware
    from synchronous_key_init import ensure_synchronous_key
    from asymmetric_key_init import ensure_asymmetric_key

    initialize_secure_hardware()
    initialize_key_store()
    ensure_synchronous_key()
    ensure_asymmetric_key()
