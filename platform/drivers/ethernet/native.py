"""Native userspace NIC backend contract.

This is intentionally a strict backend interface, not a fake register driver.
A production implementation can be backed by DPDK, AF_XDP, or another native
userspace dataplane without changing router-facing code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Packet:
    payload: bytes


class NativeNICBackend(ABC):
    """Minimal packet-I/O contract used by the router dataplane."""

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def receive(self, budget: int = 32) -> list[Packet]:
        raise NotImplementedError

    @abstractmethod
    def transmit(self, packets: list[Packet]) -> int:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class BackendUnavailable(RuntimeError):
    pass


def require_backend(name: str) -> NativeNICBackend:
    """Resolve a compiled/native backend without silently falling back."""
    if name == "dpdk":
        raise BackendUnavailable(
            "The DPDK backend requires a compiled native extension linked against the installed DPDK."
        )
    if name == "af_xdp":
        raise BackendUnavailable(
            "The AF_XDP backend requires a compiled native extension and an XDP-capable interface."
        )
    raise BackendUnavailable(f"Unsupported native backend: {name}")
