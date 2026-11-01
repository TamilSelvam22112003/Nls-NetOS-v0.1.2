"""Socket transport abstraction for Router-CA synchronization."""

class RouterCASocketClient:
    def connect(self, endpoint):
        raise NotImplementedError

    def request_metadata(self, request):
        raise NotImplementedError

    def close(self):
        pass
