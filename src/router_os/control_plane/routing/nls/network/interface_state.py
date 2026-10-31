"""Network interface state."""
from dataclasses import dataclass

@dataclass
class InterfaceState:
    name: str
    up: bool = False
    admin_up: bool = False
    carrier: bool = False
