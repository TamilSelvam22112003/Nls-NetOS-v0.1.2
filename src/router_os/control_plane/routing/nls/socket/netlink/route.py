"""Netlink route adapter."""
class RouteNetlink:
    def list(self, messages):
        return [m for m in messages if getattr(m, "message_type", None) == "route"]
