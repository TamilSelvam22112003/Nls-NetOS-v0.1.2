"""Router-CA secure connection and refresh lifecycle."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import ssl
import urllib.request

from .config import RouterCAConfig


@dataclass(frozen=True)
class RouterCAResponse:
    status: int
    body: bytes


class RouterCAClient:
    def __init__(self, config: RouterCAConfig) -> None:
        self.config = config

    def _ssl_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context(cafile=self.config.bootstrap_ca_file)
        if self.config.client_certificate_file:
            context.load_cert_chain(
                self.config.client_certificate_file,
                self.config.client_key_file,
            )
        return context

    def connect(self, path: str = "/v1/router/sync") -> RouterCAResponse:
        """Connect to the configured Router-CA over authenticated TLS."""
        self.config.validate()
        url = self.config.endpoint.rstrip("/") + path
        request = urllib.request.Request(
            url,
            method="GET",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(
            request,
            context=self._ssl_context(),
            timeout=self.config.connect_timeout_seconds,
        ) as response:
            return RouterCAResponse(response.status, response.read())


class RouterCARefreshScheduler:
    """Calculates refresh deadlines without blocking the boot sequence."""

    def __init__(self, config: RouterCAConfig) -> None:
        self.config = config
        self.last_success_at: datetime | None = None

    def mark_success(self, when: datetime | None = None) -> datetime:
        now = when or datetime.now(timezone.utc)
        self.last_success_at = now
        return now + timedelta(seconds=self.config.refresh_interval_seconds)

    def due(self, now: datetime | None = None) -> bool:
        if self.last_success_at is None:
            return True
        current = now or datetime.now(timezone.utc)
        return current >= self.last_success_at + timedelta(
            seconds=self.config.refresh_interval_seconds
        )
