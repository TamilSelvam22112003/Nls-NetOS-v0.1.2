"""Central NLS customization configuration."""
from dataclasses import dataclass, field

@dataclass
class NLSConfig:
    protocol_enabled: bool = True
    enable_ipv4: bool = True
    enable_ipv6: bool = True
    enable_neighbor_discovery: bool = True
    max_packet_size: int = 4096
    hello_interval: float = 10.0
    dead_interval: float = 40.0
    rsa_key_size: int = 3072
    interface_overrides: dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        if self.max_packet_size <= 0:
            raise ValueError("max_packet_size must be positive")
        if self.hello_interval <= 0 or self.dead_interval <= 0:
            raise ValueError("NLS timers must be positive")
        if self.dead_interval < self.hello_interval:
            raise ValueError("dead_interval must be >= hello_interval")
        if self.rsa_key_size < 3072:
            raise ValueError("NLS requires RSA-3072 or stronger")
