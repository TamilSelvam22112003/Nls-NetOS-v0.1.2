"""Key lifecycle state."""
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class KeyLifecycle:
    key_id: str
    version: int
    state: str = "active"
    created_at: datetime = datetime.now(timezone.utc)

    def activate(self) -> None:
        self.state = "active"

    def revoke(self) -> None:
        self.state = "revoked"

    def expire(self) -> None:
        self.state = "expired"
