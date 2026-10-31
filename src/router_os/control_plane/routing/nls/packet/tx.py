"""Packet transmit path."""
class PacketTransmitter:
    def send(self, sock, payload, address):
        return sock.sendto(payload, address)
