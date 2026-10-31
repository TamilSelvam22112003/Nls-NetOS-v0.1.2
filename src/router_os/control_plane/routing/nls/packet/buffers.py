"""Bounded packet buffers."""
class PacketBuffer:
    def __init__(self, max_size=4096):
        self.max_size = max_size

    def validate(self, payload: bytes):
        if len(payload) > self.max_size:
            raise ValueError("NLS packet exceeds configured maximum")
        return payload
