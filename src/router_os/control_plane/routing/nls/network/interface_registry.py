"""Runtime interface registry."""
class InterfaceRegistry:
    def __init__(self):
        self._interfaces = {}

    def add(self, interface):
        self._interfaces[interface.name] = interface

    def get(self, name):
        return self._interfaces.get(name)

    def all(self):
        return tuple(self._interfaces.values())
