"""Metadata attached to packets before protocol parsing."""
from dataclasses import dataclass

@dataclass(frozen=True)
class PacketMetadata:
    interface: str
    family: int
    source: str | None = None
    destination: str | None = None
    received_at: float | None = None
