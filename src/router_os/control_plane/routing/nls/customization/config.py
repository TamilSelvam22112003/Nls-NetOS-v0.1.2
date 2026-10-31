"""Central NLS customization points.

These defaults are intentionally protocol-specific rather than buried inside
socket, packet, or Linux-integration code.  Operators can replace the policy
object when adapting NLS to a deployment without changing the observation
engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class NLSCustomization:
    """Configuration used by the NLS network-observation subsystem."""

    protocol_name: str = "NLS"
    control_plane_protocols: FrozenSet[int] = field(default_factory=frozenset)
    managed_interface_prefixes: tuple[str, ...] = ()
    management_interface_names: FrozenSet[str] = field(default_factory=frozenset)
    lan_interface_names: FrozenSet[str] = field(default_factory=frozenset)
    wan_interface_names: FrozenSet[str] = field(default_factory=frozenset)
    point_to_point_interface_names: FrozenSet[str] = field(default_factory=frozenset)
    enable_neighbor_discovery: bool = True
    enable_socket_inventory: bool = True
    enable_netlink_monitor: bool = True
    allow_inferred_classification: bool = True

    def classify_override(self, interface_name: str) -> str | None:
        """Return an explicit NLS classification override, if configured."""
        if interface_name in self.management_interface_names:
            return "MANAGEMENT"
        if interface_name in self.lan_interface_names:
            return "LAN"
        if interface_name in self.wan_interface_names:
            return "WAN"
        if interface_name in self.point_to_point_interface_names:
            return "POINT_TO_POINT"
        return None


def load_defaults() -> NLSCustomization:
    """Return the default NLS policy.

    Deployment-specific values should be supplied by the NLS configuration
    layer; this module deliberately contains no host-specific assumptions.
    """
    return NLSCustomization()
