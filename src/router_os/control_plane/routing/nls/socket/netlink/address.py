"""Netlink address adapter."""
class AddressNetlink:
    def list(self, messages):
        return [m for m in messages if getattr(m, "message_type", None) == "address"]
