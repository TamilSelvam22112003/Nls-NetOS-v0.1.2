"""NLS key version helpers."""


def next_version(current: int) -> int:
    if current < 1:
        return 1
    return current + 1
