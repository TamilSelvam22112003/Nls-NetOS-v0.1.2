"""NLS secure-communication packet helpers.

RSA-3072 protects a small symmetric key during establishment. Synchronous
neighbor traffic keys are then used by the NLS packet layer for bulk traffic.
This module deliberately does not expose private-key export or raw synchronous
key sharing.
"""
from __future__ import annotations

from dataclasses import dataclass

from .asymmetric.rsa import RSA_BITS, RSA_CIPHERTEXT_BYTES, encrypt_key


@dataclass(frozen=True)
class RSA3072KeyEnvelope:
    algorithm: str
    key_id: str
    key_version: int
    key_epoch: int
    ciphertext: bytes

    def validate(self) -> None:
        if self.algorithm != "RSA-3072-OAEP-SHA256":
            raise ValueError("unsupported NLS RSA algorithm")
        if len(self.ciphertext) != RSA_CIPHERTEXT_BYTES:
            raise ValueError("RSA-3072 ciphertext must be exactly 384 bytes")


def wrap_synchronous_traffic_key(
    recipient_public_key,
    synchronous_traffic_key: bytes,
    *,
    key_id: str,
    key_version: int,
    key_epoch: int,
) -> RSA3072KeyEnvelope:
    """Wrap a neighbor-specific traffic key, never the global sync key."""
    ciphertext = encrypt_key(recipient_public_key, synchronous_traffic_key)
    envelope = RSA3072KeyEnvelope(
        algorithm=f"RSA-{RSA_BITS}-OAEP-SHA256",
        key_id=key_id,
        key_version=key_version,
        key_epoch=key_epoch,
        ciphertext=ciphertext,
    )
    envelope.validate()
    return envelope
