"""Alert fan-out adapters for CPU overload events."""

from __future__ import annotations

from dataclasses import dataclass
from .manager import CpuAlert


@dataclass(frozen=True)
class ResponsibilityAlert:
    target: str
    alert: CpuAlert


def fan_out(alert: CpuAlert) -> tuple[ResponsibilityAlert, ...]:
    """Create independent alert records for LAN, WAN and Router-CA.

    Actual delivery is intentionally left to the respective subsystem/event
    buses. This module does not directly modify routing or packet state.
    """
    return tuple(ResponsibilityAlert(target=t, alert=alert) for t in alert.responsibilities)
