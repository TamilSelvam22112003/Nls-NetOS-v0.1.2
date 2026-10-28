"""Safe memory allocation abstraction for control-plane Python services."""


def allocate(size):
    if size < 0:
        raise ValueError("size must be non-negative")
    return bytearray(size)


def release(_buffer):
    """Release a managed buffer by dropping the caller's reference."""
    return None
