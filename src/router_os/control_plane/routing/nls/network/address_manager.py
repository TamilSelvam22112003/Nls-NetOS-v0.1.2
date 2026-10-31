"""Interface address management boundary."""
class AddressManager:
    def __init__(self):
        self.addresses = {}

    def set(self, interface, addresses):
        self.addresses[interface] = tuple(addresses)
