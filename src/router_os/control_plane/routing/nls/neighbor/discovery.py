"""NLS one-hop neighbor discovery.

This module accepts already-decoded NLS hello/neighbor advertisements. It does
not perform raw socket I/O or cryptographic authentication; those concerns
belong to the packet and security layers. Discovery maintains the control-plane
view of directly reachable NLS peers and records the latest authenticated
observation supplied by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from threading import RLock
from typing import Iterable, Mapping


@dataclass(frozen=True, slots=True)
class NeighborAdvertisement:
    """A decoded one-hop neighbor advertisement."""

    neighbor_id: int
    interface_id: str
    neighbor_ip: str
    key_id: int
    link_state: str = "INIT"
    authenticated: bool = False
    observed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.neighbor_id <= 0xFFFFFFFF:
            raise ValueError("neighbor_id must be a UINT32 value")
        if not self.interface_id or len(self.interface_id) > 32:
            raise ValueError("interface_id must contain 1..32 characters")
        if not self.neighbor_ip or len(self.neighbor_ip) > 64:
            raise ValueError("neighbor_ip must contain 1..64 characters")
        if not 0 <= self.key_id <= 0xFFFFFFFF:
            raise ValueError("key_id must be a UINT32 value")
        if self.link_state not in {"DOWN", "INIT", "2-WAY", "FULL"}:
            raise ValueError("unsupported NLS neighbor link state")

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "NeighborAdvertisement":
        """Build an advertisement from a decoded packet/message mapping."""
        return cls(
            neighbor_id=int(value["neighbor_id"]),
            interface_id=str(value["interface_id"]),
            neighbor_ip=str(value["neighbor_ip"]),
            key_id=int(value["key_id"]),
            link_state=str(value.get("link_state", "INIT")),
            authenticated=bool(value.get("authenticated", False)),
            observed_at=value.get("observed_at") if isinstance(value.get("observed_at"), datetime) else None,
        )


class NeighborDiscovery:
    """Thread-safe registry of directly discovered NLS neighbors."""

    def __init__(self) -> None:
        self._neighbors: dict[tuple[int, str], NeighborAdvertisement] = {}
        self._lock = RLock()

    def observe(self, advertisement: NeighborAdvertisement) -> NeighborAdvertisement:
        """Record an observation and return the current neighbor record.

        Only authenticated advertisements are admitted into the active neighbor
        registry. The packet/security layer must set ``authenticated=True``
        after verification.
        """
        if not advertisement.authenticated:
            raise ValueError("neighbor advertisement must be authenticated before admission")

        observed_at = advertisement.observed_at or datetime.now(timezone.utc)
        current = replace(advertisement, observed_at=observed_at)
        key = (current.neighbor_id, current.interface_id)
        with self._lock:
            self._neighbors[key] = current
        return current

    def observe_mapping(self, value: Mapping[str, object]) -> NeighborAdvertisement:
        return self.observe(NeighborAdvertisement.from_mapping(value))

    def get(self, neighbor_id: int, interface_id: str) -> NeighborAdvertisement | None:
        with self._lock:
            return self._neighbors.get((neighbor_id, interface_id))

    def all(self) -> tuple[NeighborAdvertisement, ...]:
        with self._lock:
            return tuple(self._neighbors.values())

    def remove(self, neighbor_id: int, interface_id: str) -> bool:
        with self._lock:
            return self._neighbors.pop((neighbor_id, interface_id), None) is not None

    def replace_all(self, neighbors: Iterable[NeighborAdvertisement]) -> None:
        with self._lock:
            self._neighbors = {
                (item.neighbor_id, item.interface_id): item for item in neighbors
            }
