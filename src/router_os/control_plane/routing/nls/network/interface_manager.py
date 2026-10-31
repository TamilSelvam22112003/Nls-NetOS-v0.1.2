"""Interface management facade."""
class InterfaceManager:
    def __init__(self, registry):
        self.registry = registry

    def get(self, name):
        return self.registry.get(name)
