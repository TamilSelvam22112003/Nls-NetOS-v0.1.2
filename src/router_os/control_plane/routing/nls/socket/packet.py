"""Socket-level packet send/receive helpers."""
def send_packet(sock, payload: bytes, address):
    if not isinstance(payload, bytes):
        raise TypeError("payload must be bytes")
    return sock.sendto(payload, address)

def receive_packet(sock, size: int = 65535):
    return sock.recvfrom(size)
