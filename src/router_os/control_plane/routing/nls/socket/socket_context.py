"""Runtime context associated with an NLS socket."""
from dataclasses import dataclass
from .socket_state import SocketState

@dataclass
class SocketContext:
    socket_id: str
    family: int
    protocol: int
    interface: str
    state: SocketState = SocketState.CREATED
