class CryptoSubsystem:
    """Lifecycle-only crypto boundary for bootstrap v0.1.2.

    No secret material is generated, stored, exported, or logged here.
    """

    def __init__(self) -> None:
        self.initialized = False
        self.started = False

    def initialize(self) -> None:
        self.initialized = True

    def start(self) -> None:
        if not self.initialized:
            raise RuntimeError("crypto subsystem must be initialized before start")
        self.started = True

    def stop(self) -> None:
        self.started = False
        self.initialized = False
