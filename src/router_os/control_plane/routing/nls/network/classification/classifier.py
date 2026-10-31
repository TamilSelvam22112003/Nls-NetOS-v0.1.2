"""Classify interfaces using deployment policy and Linux naming hints."""
from ...customization.interface_policy import InterfaceRole

def classify(name: str) -> InterfaceRole:
    n = name.lower()
    if n == "lo": return InterfaceRole.LOOPBACK
    if n.startswith(("mgmt", "management")): return InterfaceRole.MANAGEMENT
    if n.startswith(("wan", "ppp")): return InterfaceRole.WAN
    if n.startswith(("p2p", "tun")): return InterfaceRole.P2P
    if n.startswith(("lan", "br", "eth", "en", "ens")): return InterfaceRole.LAN
    return InterfaceRole.UNKNOWN
