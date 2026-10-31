"""Netlink socket abstraction."""
import socket

NETLINK_ROUTE = 0

def create_netlink_socket(protocol: int = NETLINK_ROUTE):
    return socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, protocol)
