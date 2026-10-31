"""LAN/WAN/P2P and management interface policy."""
from dataclasses import dataclass
from enum import Enum

class InterfaceRole(str, Enum):
    LAN = "lan"
    WAN = "wan"
    P2P = "p2p"
    LOOPBACK = "loopback"
    MANAGEMENT = "management"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class InterfacePolicy:
    role: InterfaceRole = InterfaceRole.UNKNOWN
    nls_enabled: bool = True
    passive: bool = False
    neighbor_discovery: bool = True

    def allows_nls(self) -> bool:
        return self.nls_enabled and not self.passive
