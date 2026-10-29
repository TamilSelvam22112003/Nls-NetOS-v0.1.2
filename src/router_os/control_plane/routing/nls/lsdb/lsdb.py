"""Thread-safe in-memory NLS Link State Database.

The LSDB accepts validated advertisements from the NLS control plane. It does
not receive raw packets and does not perform authentication itself.
"""

from __future__ import annotations

from threading import RLock
from typing import Iterable

from .entry import LsdbEntry


class Lsdb:
    """Maintain the newest LSA for each NLS LSA identity."""

    def __init__(self) -> None:
        self._entries: dict[tuple[int, int, int], LsdbEntry] = {}
        self._lock = RLock()

    @staticmethod
    def _newer(candidate: int, current: int) -> bool:
        """Return whether candidate is newer in signed INT32 sequence space."""
        if candidate == current:
            return False
        # NLS sequence numbers are signed INT32 values. Comparing their
        # unsigned bit representations provides the protocol ordering across
        # the signed SQL representation.
        return (candidate & 0xFFFFFFFF) > (current & 0xFFFFFFFF)

    def install(self, entry: LsdbEntry) -> bool:
        """Install an LSA only when it is new or newer than the current one."""
        with self._lock:
            current = self._entries.get(entry.identity)
            if current is not None and not self._newer(
                entry.ls_sequence_number, current.ls_sequence_number
            ):
                return False
            self._entries[entry.identity] = entry
            return True

    def get(self, ls_type: int, link_state_id: int, advertising_router: int) -> LsdbEntry | None:
        with self._lock:
            return self._entries.get((ls_type, link_state_id, advertising_router))

    def all(self) -> tuple[LsdbEntry, ...]:
        with self._lock:
            return tuple(self._entries.values())

    def by_neighbor(self, neighbor_id: int) -> tuple[LsdbEntry, ...]:
        with self._lock:
            return tuple(
                entry for entry in self._entries.values()
                if entry.source_neighbor_id == neighbor_id
            )

    def remove(self, ls_type: int, link_state_id: int, advertising_router: int) -> bool:
        with self._lock:
            return self._entries.pop((ls_type, link_state_id, advertising_router), None) is not None

    def replace_all(self, entries: Iterable[LsdbEntry]) -> None:
        with self._lock:
            self._entries = {entry.identity: entry for entry in entries}
