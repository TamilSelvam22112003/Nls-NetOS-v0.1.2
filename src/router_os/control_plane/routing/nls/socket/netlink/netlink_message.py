"""Minimal Netlink message representation."""
from dataclasses import dataclass, field

@dataclass
class NetlinkMessage:
    message_type: int
    flags: int = 0
    sequence: int = 0
    payload: bytes = b""
    attributes: dict = field(default_factory=dict)
