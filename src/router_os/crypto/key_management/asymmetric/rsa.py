"""RSA-3072 primitives used by NLS secure communication.

RSA is used only for small key material. NLS bulk traffic is encrypted with
an authenticated symmetric cipher. Private keys are never returned by the
communication API.
"""
from __future__ import annotations

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

RSA_BITS = 3072
RSA_CIPHERTEXT_BYTES = RSA_BITS // 8


def generate_private_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=RSA_BITS)


def public_key_der(public_key: rsa.RSAPublicKey) -> bytes:
    return public_key.public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def private_key_der(private_key: rsa.RSAPrivateKey) -> bytes:
    return private_key.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )


def encrypt_key(recipient_public_key: rsa.RSAPublicKey, key_material: bytes) -> bytes:
    """RSA-OAEP-SHA256 encrypt small key material; ciphertext is always 384 B."""
    return recipient_public_key.encrypt(
        key_material,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_key(private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
    if len(ciphertext) != RSA_CIPHERTEXT_BYTES:
        raise ValueError("RSA-3072 ciphertext must be exactly 384 bytes")
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
