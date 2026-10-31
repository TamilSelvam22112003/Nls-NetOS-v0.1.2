"""Observed network inventory."""
class NetworkInventory:
    def __init__(self):
        self.interfaces = {}

    def replace(self, interfaces):
        self.interfaces = dict(interfaces)
