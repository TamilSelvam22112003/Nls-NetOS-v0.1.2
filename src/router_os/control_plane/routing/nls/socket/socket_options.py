"""NLS socket options."""
from dataclasses import dataclass

@dataclass
class SocketOptions:
    reuse_address: bool = True
    receive_buffer: int = 262144
    send_buffer: int = 262144
    multicast: bool = False
