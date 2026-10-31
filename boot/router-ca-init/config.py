"""Router-CA boot configuration.

The endpoint is a management/synchronization transport. The NLS Router-CA
packet format is deliberately not defined here.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RouterCAConfig:
    enabled: bool = True
    home_ca_alias: str = "manufacturer-router-ca"
    endpoint: str = "https://router-ca.example.invalid"
    refresh_interval_seconds: int = 3600
    connect_timeout_seconds: float = 10.0
    bootstrap_ca_file: str | None = None
    client_certificate_file: str | None = None
    client_key_file: str | None = None
    state_file: str = "/var/lib/nls/router-ca-state.json"

    def validate(self) -> None:
        if not self.enabled:
            return
        if not self.endpoint.startswith("https://"):
            raise ValueError("Router-CA endpoint must use HTTPS")
        if self.refresh_interval_seconds <= 0:
            raise ValueError("refresh_interval_seconds must be positive")
        if self.connect_timeout_seconds <= 0:
            raise ValueError("connect_timeout_seconds must be positive")
