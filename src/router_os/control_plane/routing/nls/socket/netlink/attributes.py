"""Netlink attribute helpers."""
def get_attribute(attributes, name, default=None):
    return attributes.get(name, default)
