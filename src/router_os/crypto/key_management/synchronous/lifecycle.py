"""Synchronous key lifecycle facade."""
from ..key_lifecycle import KeyLifecycle


def lifecycle(key):
    return KeyLifecycle(key.key_id, key.version)
