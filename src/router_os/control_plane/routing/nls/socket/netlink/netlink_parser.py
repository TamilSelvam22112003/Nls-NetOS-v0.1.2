"""Netlink message parser boundary."""
class NetlinkParser:
    def parse(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError("Netlink data must be bytes")
        return data
