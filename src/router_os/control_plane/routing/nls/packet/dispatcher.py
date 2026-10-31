"""Packet dispatcher."""
class PacketDispatcher:
    def __init__(self):
        self.handlers = {}

    def register(self, packet_type, handler):
        self.handlers[packet_type] = handler

    def dispatch(self, packet):
        handler = self.handlers.get(getattr(packet, "packet_type", None))
        if handler is None:
            raise ValueError("No handler registered for packet type")
        return handler(packet)
