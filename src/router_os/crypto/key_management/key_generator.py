"""Cryptographic key generation primitives for NLS-NetOS."""
from __future__ import annotations

import secrets

from .asymmetric.rsa import generate_private_key, private_key_der, public_key_der


class KeyGenerator:
    """Generate NLS key material without persisting it."""

    @staticmethod
    def synchronous_key(size: int = 32) -> bytes:
        if size < 32:
            raise ValueError("NLS synchronous keys must be at least 256 bits")
        return secrets.token_bytes(size)

    @staticmethod
    def asymmetric_keypair() -> tuple[bytes, bytes]:
        """Generate the NLS RSA-3072 identity key pair as DER bytes."""
        private = generate_private_key()
        return private_key_der(private), public_key_der(private.public_key())
