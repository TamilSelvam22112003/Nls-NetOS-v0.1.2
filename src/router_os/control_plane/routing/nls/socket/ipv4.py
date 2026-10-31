"""IPv4 socket helpers."""
import socket

PROTOCOL_NLS = 253

def create_ipv4_socket(raw: bool = False):
    kind = socket.SOCK_RAW if raw else socket.SOCK_DGRAM
    return socket.socket(socket.AF_INET, kind, PROTOCOL_NLS if raw else 0)
