"""Socket lifecycle events."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SocketEvent:
    kind: str
    socket_id: str
    detail: str = ""
