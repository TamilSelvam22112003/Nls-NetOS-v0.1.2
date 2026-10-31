"""Boot-time Router-CA initialization."""

from .client import RouterCAClient, RouterCARefreshScheduler
from .config import RouterCAConfig
from .database import RouterCADatabase


class RouterCAStartup:
    def __init__(
        self,
        config: RouterCAConfig | None = None,
        database: RouterCADatabase | None = None,
    ) -> None:
        self.config = config or RouterCAConfig()
        self.database = database or RouterCADatabase()
        self.client = RouterCAClient(self.config)
        self.scheduler = RouterCARefreshScheduler(self.config)

    def initialize(self) -> None:
        """Load persistent trust-anchor metadata before network synchronization."""
        if not self.config.enabled:
            return
        self.config.validate()
        self.database.open()

    def synchronize(self) -> bytes:
        """Perform the first Router-CA synchronization after networking is ready."""
        response = self.client.connect()
        self.scheduler.mark_success()
        return response.body

    def refresh_due(self) -> bool:
        return self.scheduler.due()
