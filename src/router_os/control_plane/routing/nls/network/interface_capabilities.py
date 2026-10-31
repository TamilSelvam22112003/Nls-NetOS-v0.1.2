"""Interface capabilities used by NLS policy."""
from dataclasses import dataclass

@dataclass(frozen=True)
class InterfaceCapabilities:
    ipv4: bool = True
    ipv6: bool = True
    multicast: bool = True
    raw_socket: bool = True
