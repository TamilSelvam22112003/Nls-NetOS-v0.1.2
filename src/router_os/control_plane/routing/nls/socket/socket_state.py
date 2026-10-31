"""NLS socket state."""
from enum import Enum

class SocketState(str, Enum):
    CREATED = "created"
    BOUND = "bound"
    LISTENING = "listening"
    CONNECTED = "connected"
    CLOSED = "closed"
    ERROR = "error"
