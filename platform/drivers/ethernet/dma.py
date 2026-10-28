"""Packet DMA abstractions for Ethernet datapaths.

The implementation owns aligned userspace buffers and queue accounting. Actual
NIC DMA mapping remains the responsibility of the kernel/native backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass
class DMABuffer:
    data: bytearray
    dma_address: int | None = None
    mapped: bool = False

    @property
    def length(self) -> int:
        return len(self.data)


class DMAQueue:
    def __init__(self, depth: int = 1024) -> None:
        if depth < 1:
            raise ValueError("depth must be positive")
        self.depth = depth
        self._buffers: list[DMABuffer] = []
        self._lock = Lock()
        self.submitted = 0
        self.completed = 0

    def allocate(self, size: int) -> DMABuffer:
        if size < 0:
            raise ValueError("size must be non-negative")
        return DMABuffer(bytearray(size))

    def submit(self, buffer: DMABuffer) -> bool:
        with self._lock:
            if len(self._buffers) >= self.depth:
                return False
            buffer.mapped = True
            self._buffers.append(buffer)
            self.submitted += 1
            return True

    def complete(self) -> DMABuffer | None:
        with self._lock:
            if not self._buffers:
                return None
            buffer = self._buffers.pop(0)
            buffer.mapped = False
            self.completed += 1
            return buffer

    @property
    def pending(self) -> int:
        with self._lock:
            return len(self._buffers)
