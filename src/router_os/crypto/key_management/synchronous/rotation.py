"""Synchronous key rotation facade."""
from ..key_rotation import KeyRotation


def rotate():
    return KeyRotation().rotate_synchronous()
