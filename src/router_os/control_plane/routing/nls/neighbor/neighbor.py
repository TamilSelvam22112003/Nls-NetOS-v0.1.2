"""NLS neighbor state model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


VALID_LINK_STATES = frozenset({"DOWN", "INIT", "2-WAY", "FULL"})


@dataclass(frozen=True, slots=True)
class Neighbor:
    """Control-plane identity and current state of a one-hop NLS peer."""

    neighbor_id: int
    interface_id: str
    neighbor_ip: str
    key_id: int
    link_state: str = "DOWN"
    last_seen_timestamp: datetime | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.neighbor_id <= 0xFFFFFFFF:
            raise ValueError("neighbor_id must be a UINT32 value")
        if not self.interface_id or len(self.interface_id) > 32:
            raise ValueError("interface_id must contain 1..32 characters")
        if not self.neighbor_ip or len(self.neighbor_ip) > 64:
            raise ValueError("neighbor_ip must contain 1..64 characters")
        if not 0 <= self.key_id <= 0xFFFFFFFF:
            raise ValueError("key_id must be a UINT32 value")
        if self.link_state not in VALID_LINK_STATES:
            raise ValueError("unsupported NLS neighbor link state")

    @property
    def identity(self) -> tuple[int, str]:
        return self.neighbor_id, self.interface_id
