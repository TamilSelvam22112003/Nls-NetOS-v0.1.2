"""Address abstraction used by NLS sockets."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SocketAddress:
    address: str
    port: int = 0
    interface: str | None = None
