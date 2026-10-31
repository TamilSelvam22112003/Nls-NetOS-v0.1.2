"""Packet engine connecting socket RX/TX to NLS dispatch."""
class PacketEngine:
    def __init__(self, rx, tx, dispatcher):
        self.rx, self.tx, self.dispatcher = rx, tx, dispatcher

    def process(self, packet):
        return self.dispatcher.dispatch(packet)
