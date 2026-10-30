"""Asymmetric identity-key generation."""
from ..key_generator import KeyGenerator


def generate() -> tuple[bytes, bytes]:
    return KeyGenerator.asymmetric_keypair()
