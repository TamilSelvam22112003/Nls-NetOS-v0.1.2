"""Netlink neighbor adapter."""
class NeighborNetlink:
    def list(self, messages):
        return [m for m in messages if getattr(m, "message_type", None) == "neighbor"]
