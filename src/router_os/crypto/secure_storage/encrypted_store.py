"""Encrypted software-backed storage for development fallback.

The wrapping key must come from an external secret-management mechanism; it is
never stored beside the encrypted records. Production should prefer TPM/HSM/SE.
"""
from __future__ import annotations
import os

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:  # pragma: no cover
    AESGCM = None


class EncryptedStore:
    def __init__(self, wrapping_key: bytes):
        if AESGCM is None:
            raise RuntimeError("cryptography package is required")
        if len(wrapping_key) not in (16, 24, 32):
            raise ValueError("wrapping key must be 128, 192, or 256 bits")
        self._aead = AESGCM(wrapping_key)

    def encrypt(self, plaintext: bytes, aad: bytes = b"nls-router") -> bytes:
        nonce = os.urandom(12)
        return nonce + self._aead.encrypt(nonce, plaintext, aad)

    def decrypt(self, ciphertext: bytes, aad: bytes = b"nls-router") -> bytes:
        if len(ciphertext) < 13:
            raise ValueError("invalid encrypted record")
        return self._aead.decrypt(ciphertext[:12], ciphertext[12:], aad)
