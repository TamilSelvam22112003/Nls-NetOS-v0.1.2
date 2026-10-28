"""Continuous CPU guard monitoring loop."""

from __future__ import annotations

from typing import Callable

from .manager import CpuGuard, sample_utilization


class CpuMonitor:
    def __init__(self, guard: CpuGuard, interval: float = 1.0,
                 on_alert: Callable[[object], None] | None = None) -> None:
        self.guard = guard
        self.interval = max(0.1, interval)
        self.on_alert = on_alert
        self.running = False

    def run_once(self) -> list[object]:
        alerts = []
        for cpu, utilization in sample_utilization(self.interval).items():
            alert = self.guard.evaluate(cpu, utilization)
            if alert is not None:
                alerts.append(alert)
                if self.on_alert is not None:
                    self.on_alert(alert)
        return alerts
