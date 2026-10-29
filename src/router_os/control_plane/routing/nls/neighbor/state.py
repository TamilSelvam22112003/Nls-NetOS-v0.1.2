"""Thread-safe in-memory state for discovered NLS neighbors."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock

from .neighbor import Neighbor, VALID_LINK_STATES


class NeighborStateStore:
    """Maintain the latest state for each directly connected NLS neighbor."""

    def __init__(self) -> None:
        self._items: dict[tuple[int, str], Neighbor] = {}
        self._lock = RLock()

    def upsert(
        self,
        *,
        neighbor_id: int,
        interface_id: str,
        neighbor_ip: str,
        key_id: int,
        link_state: str,
        seen_at: datetime | None = None,
    ) -> Neighbor:
        if link_state not in VALID_LINK_STATES:
            raise ValueError("unsupported NLS neighbor link state")
        item = Neighbor(
            neighbor_id=neighbor_id,
            interface_id=interface_id,
            neighbor_ip=neighbor_ip,
            key_id=key_id,
            link_state=link_state,
            last_seen_timestamp=seen_at or datetime.now(timezone.utc),
        )
        with self._lock:
            self._items[item.identity] = item
        return item

    def get(self, neighbor_id: int, interface_id: str) -> Neighbor | None:
        with self._lock:
            return self._items.get((neighbor_id, interface_id))

    def all(self) -> tuple[Neighbor, ...]:
        with self._lock:
            return tuple(self._items.values())

    def remove(self, neighbor_id: int, interface_id: str) -> bool:
        with self._lock:
            return self._items.pop((neighbor_id, interface_id), None) is not None
