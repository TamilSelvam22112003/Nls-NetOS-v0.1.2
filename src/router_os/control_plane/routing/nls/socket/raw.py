"""Raw packet socket creation."""
import socket

def create_raw_packet_socket(protocol: int):
    return socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)
