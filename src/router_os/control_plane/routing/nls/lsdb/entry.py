"""NLS Link State Database entry model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class LsdbEntry:
    """One current LSA version in the NLS LSDB."""

    ls_type: int
    link_state_id: int
    advertising_router: int
    ls_age: int
    ls_sequence_number: int
    ls_checksum: int
    length: int
    payload: bytes = b""
    link_count: int | None = None
    source_neighbor_id: int | None = None
    installed_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.ls_type <= 0xFFFF:
            raise ValueError("ls_type must be a UINT16 value")
        for name, value in (("link_state_id", self.link_state_id), ("advertising_router", self.advertising_router)):
            if not 0 <= value <= 0xFFFFFFFF:
                raise ValueError(f"{name} must be a UINT32 value")
        if not 0 <= self.ls_age <= 3600:
            raise ValueError("ls_age must be between 0 and 3600 seconds")
        if not -(2**31) <= self.ls_sequence_number <= 2**31 - 1:
            raise ValueError("ls_sequence_number must be a signed INT32 value")
        if not 0 <= self.ls_checksum <= 0xFFFF:
            raise ValueError("ls_checksum must be a UINT16 value")
        if not 0 < self.length <= 0xFFFF:
            raise ValueError("length must be between 1 and 65535")
        if self.link_count is not None and self.link_count < 0:
            raise ValueError("link_count cannot be negative")
        if self.source_neighbor_id is not None and not 0 <= self.source_neighbor_id <= 0xFFFFFFFF:
            raise ValueError("source_neighbor_id must be a UINT32 value")
        if not isinstance(self.payload, bytes):
            raise TypeError("payload must be bytes")

    @property
    def identity(self) -> tuple[int, int, int]:
        return self.ls_type, self.link_state_id, self.advertising_router

    @property
    def payload_length(self) -> int:
        return len(self.payload)
