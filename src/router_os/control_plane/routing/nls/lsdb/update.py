"""Bridge authenticated neighbor advertisements into the NLS LSDB."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping

from ..neighbor.discovery import NeighborAdvertisement
from ..neighbor.state import NeighborStateStore
from .entry import LsdbEntry
from .lsdb import Lsdb


@dataclass(frozen=True, slots=True)
class LsdbUpdateResult:
    neighbor_updated: bool
    lsa_installed: bool


class LsdbUpdateService:
    """Process decoded, authenticated one-hop advertisements."""

    def __init__(self, lsdb: Lsdb, neighbors: NeighborStateStore) -> None:
        self.lsdb = lsdb
        self.neighbors = neighbors

    def process_neighbor_lsa(
        self,
        *,
        advertisement: NeighborAdvertisement,
        ls_type: int,
        link_state_id: int,
        advertising_router: int,
        ls_age: int,
        ls_sequence_number: int,
        ls_checksum: int,
        length: int,
        payload: bytes,
        link_count: int | None = None,
    ) -> LsdbUpdateResult:
        """Update neighbor state and install a newer LSA from that neighbor."""
        if not advertisement.authenticated:
            raise ValueError("unauthenticated neighbor advertisement cannot update LSDB")
        if advertising_router != advertisement.neighbor_id:
            raise ValueError("advertising_router does not match the authenticated neighbor")

        seen_at = advertisement.observed_at or datetime.now(timezone.utc)
        self.neighbors.upsert(
            neighbor_id=advertisement.neighbor_id,
            interface_id=advertisement.interface_id,
            neighbor_ip=advertisement.neighbor_ip,
            key_id=advertisement.key_id,
            link_state=advertisement.link_state,
            seen_at=seen_at,
        )

        entry = LsdbEntry(
            ls_type=ls_type,
            link_state_id=link_state_id,
            advertising_router=advertising_router,
            ls_age=ls_age,
            ls_sequence_number=ls_sequence_number,
            ls_checksum=ls_checksum,
            length=length,
            payload=payload,
            link_count=link_count,
            source_neighbor_id=advertisement.neighbor_id,
            installed_at=seen_at,
            updated_at=seen_at,
        )
        installed = self.lsdb.install(entry)
        return LsdbUpdateResult(neighbor_updated=True, lsa_installed=installed)

    def process_mapping(self, value: Mapping[str, object]) -> LsdbUpdateResult:
        """Convenience adapter for an already-decoded NLS message mapping."""
        advertisement = NeighborAdvertisement.from_mapping(value)
        payload = value.get("payload", b"")
        if not isinstance(payload, bytes):
            raise TypeError("payload must be bytes")
        return self.process_neighbor_lsa(
            advertisement=advertisement,
            ls_type=int(value["ls_type"]),
            link_state_id=int(value["link_state_id"]),
            advertising_router=int(value.get("advertising_router", advertisement.neighbor_id)),
            ls_age=int(value.get("ls_age", 0)),
            ls_sequence_number=int(value["ls_sequence_number"]),
            ls_checksum=int(value["ls_checksum"]),
            length=int(value["length"]),
            payload=payload,
            link_count=int(value["link_count"]) if value.get("link_count") is not None else None,
        )
