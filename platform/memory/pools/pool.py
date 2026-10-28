"""Reusable object pool for packet/control-plane allocations."""
from collections import deque


class ObjectPool:
    def __init__(self, factory, max_size=1024):
        if max_size < 1:
            raise ValueError("max_size must be positive")
        self._factory = factory
        self._max_size = max_size
        self._free = deque()

    def acquire(self):
        return self._free.pop() if self._free else self._factory()

    def release(self, obj):
        if len(self._free) < self._max_size:
            self._free.append(obj)

    def clear(self):
        self._free.clear()
