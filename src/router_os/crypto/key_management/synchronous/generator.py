"""Synchronous-key generation."""
from ..key_generator import KeyGenerator


def generate(size: int = 32) -> bytes:
    return KeyGenerator.synchronous_key(size)
