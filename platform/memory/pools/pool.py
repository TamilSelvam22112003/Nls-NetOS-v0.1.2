"""Reusable, bounded and thread-safe object pools."""

from __future__ import annotations

from collections import deque
from threading import Lock
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class ObjectPool(Generic[T]):
    def __init__(self, factory: Callable[[], T], max_size: int = 1024) -> None:
        if max_size < 1:
            raise ValueError("max_size must be positive")
        self._factory = factory
        self._max_size = max_size
        self._free: deque[T] = deque()
        self._created = 0
        self._lock = Lock()

    def acquire(self) -> T:
        with self._lock:
            if self._free:
                return self._free.pop()
            self._created += 1
        return self._factory()

    def release(self, obj: T) -> bool:
        with self._lock:
            if len(self._free) >= self._max_size:
                return False
            self._free.append(obj)
            return True

    def clear(self) -> int:
        with self._lock:
            count = len(self._free)
            self._free.clear()
            return count

    @property
    def free_count(self) -> int:
        with self._lock:
            return len(self._free)

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def created_count(self) -> int:
        with self._lock:
            return self._created
