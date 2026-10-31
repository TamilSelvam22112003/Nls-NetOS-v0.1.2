"""Packet receive path."""
class PacketReceiver:
    def receive(self, sock, size=65535):
        return sock.recvfrom(size)
