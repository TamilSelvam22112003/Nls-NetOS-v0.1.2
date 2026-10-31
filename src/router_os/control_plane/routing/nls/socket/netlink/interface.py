"""Netlink interface inventory adapter."""
class InterfaceNetlink:
    def list(self, messages):
        return [m for m in messages if getattr(m, "message_type", None) == "interface"]
