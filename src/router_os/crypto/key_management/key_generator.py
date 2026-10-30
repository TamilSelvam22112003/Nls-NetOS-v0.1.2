"""Cryptographic key generation primitives for NLS-NetOS."""
from __future__ import annotations

import secrets

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
except ImportError:  # pragma: no cover
    Ed25519PrivateKey = None


class KeyGenerator:
    """Generate key material without persisting it."""

    @staticmethod
    def synchronous_key(size: int = 32) -> bytes:
        return secrets.token_bytes(size)

    @staticmethod
    def asymmetric_keypair() -> tuple[bytes, bytes]:
        if Ed25519PrivateKey is None:
            raise RuntimeError("cryptography package is required for asymmetric keys")
        private = Ed25519PrivateKey.generate()
        return (
            private.private_bytes_raw(),
            private.public_key().public_bytes_raw(),
        )
