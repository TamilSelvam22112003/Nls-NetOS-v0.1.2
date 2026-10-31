"""Netlink link-state adapter."""
class LinkNetlink:
    def list(self, messages):
        return [m for m in messages if getattr(m, "message_type", None) == "link"]
