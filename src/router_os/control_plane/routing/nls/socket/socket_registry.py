"""Registry of active NLS socket contexts."""
class SocketRegistry:
    def __init__(self):
        self._sockets = {}

    def add(self, context):
        self._sockets[context.socket_id] = context
        return context

    def remove(self, socket_id):
        return self._sockets.pop(socket_id, None)

    def get(self, socket_id):
        return self._sockets.get(socket_id)

    def all(self):
        return tuple(self._sockets.values())
