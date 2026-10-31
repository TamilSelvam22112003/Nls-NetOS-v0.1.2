"""Lifecycle manager for NLS sockets."""
from .socket_registry import SocketRegistry

class SocketManager:
    def __init__(self):
        self.registry = SocketRegistry()

    def register(self, context):
        return self.registry.add(context)

    def close(self, socket_id):
        return self.registry.remove(socket_id)
