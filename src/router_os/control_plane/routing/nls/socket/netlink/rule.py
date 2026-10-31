"""Netlink policy-rule adapter."""
class RuleNetlink:
    def list(self, messages):
        return [m for m in messages if getattr(m, "message_type", None) == "rule"]
