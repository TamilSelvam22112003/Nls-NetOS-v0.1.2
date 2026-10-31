"""Kernel neighbor inventory boundary."""
class NeighborManager:
    def __init__(self):
        self.neighbors = {}

    def update(self, key, value):
        self.neighbors[key] = value
