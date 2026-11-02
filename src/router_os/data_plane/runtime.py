from router_os.config import NetOSConfig


class DataPlaneSubsystem:
    """Lifecycle boundary; packet forwarding is a later milestone."""

    def __init__(self, config: NetOSConfig) -> None:
        self.config = config
        self.initialized = False
        self.started = False

    def initialize(self) -> None:
        self.initialized = True

    def start(self) -> None:
        if not self.initialized:
            raise RuntimeError("data plane must be initialized before start")
        self.started = True

    def stop(self) -> None:
        self.started = False
        self.initialized = False
