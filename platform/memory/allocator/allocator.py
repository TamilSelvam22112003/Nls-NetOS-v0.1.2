"""Managed memory allocation primitives for NLS-NetOS services."""

from __future__ import annotations

from dataclasses import dataclass
import threading


@dataclass
class Allocation:
    """Owned allocation with explicit size and lifecycle state."""

    buffer: bytearray
    alignment: int = 1
    released: bool = False

    @property
    def size(self) -> int:
        return len(self.buffer)

    def release(self) -> None:
        if not self.released:
            self.buffer.clear()
            self.released = True


class MemoryAllocator:
    """Thread-safe allocator with accounting and optional byte limit."""

    def __init__(self, limit: int | None = None) -> None:
        if limit is not None and limit < 0:
            raise ValueError("limit must be non-negative")
        self.limit = limit
        self.used = 0
        self._lock = threading.Lock()

    def allocate(self, size: int, alignment: int = 1) -> Allocation:
        if size < 0:
            raise ValueError("size must be non-negative")
        if alignment < 1 or alignment & (alignment - 1):
            raise ValueError("alignment must be a positive power of two")
        with self._lock:
            if self.limit is not None and self.used + size > self.limit:
                raise MemoryError("allocator limit exceeded")
            allocation = Allocation(bytearray(size), alignment)
            self.used += size
            return allocation

    def release(self, allocation: Allocation) -> None:
        with self._lock:
            if allocation.released:
                return
            size = allocation.size
            allocation.release()
            self.used = max(0, self.used - size)

    @property
    def available(self) -> int | None:
        return None if self.limit is None else self.limit - self.used


_default = MemoryAllocator()


def allocate(size: int, alignment: int = 1) -> bytearray:
    """Compatibility helper returning a raw bytearray."""
    return _default.allocate(size, alignment).buffer


def release(_buffer: bytearray) -> None:
    """Release a raw buffer by dropping the caller's reference."""
    return None
