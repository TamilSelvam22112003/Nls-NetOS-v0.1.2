"""CPU reservation and overload monitoring.

The guard reserves the last logical CPU when the system has an odd number of
logical CPUs >= 3. The reserved CPU is deliberately kept out of the routing
worker affinity set. It is not disabled: Linux may still schedule kernel work
or unrelated processes there. Packet/routing workers must honor the returned
allowed CPU set.

When any non-reserved CPU reaches the warning threshold, a structured alert
is emitted for LAN, WAN and Router-CA consumers. At 100%, the alert is marked
critical. Consumers can register callbacks without coupling this module to
those subsystems.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
import time
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class CpuAlert:
    cpu: int
    utilization: float
    severity: str
    responsibilities: tuple[str, ...] = ("LAN", "WAN", "Router-CA")


class CpuGuard:
    WARNING = 90.0
    CRITICAL = 100.0

    def __init__(self, cpu_count: int | None = None) -> None:
        self.cpu_count = cpu_count if cpu_count is not None else (os.cpu_count() or 1)
        self.reserved_cpu = self._select_reserved_cpu(self.cpu_count)
        self.routing_cpus = tuple(c for c in range(self.cpu_count) if c != self.reserved_cpu)
        self._callbacks: list[Callable[[CpuAlert], None]] = []

    @staticmethod
    def _select_reserved_cpu(count: int) -> int | None:
        if count >= 3 and count % 2 == 1:
            return count - 1
        return None

    def register_alert_callback(self, callback: Callable[[CpuAlert], None]) -> None:
        self._callbacks.append(callback)

    def affinity_mask(self) -> tuple[int, ...]:
        """CPUs that routing/packet workers are allowed to use."""
        return self.routing_cpus

    def state(self, cpu: int) -> str:
        if cpu == self.reserved_cpu:
            return "NULL"
        if cpu in self.routing_cpus:
            return "ACTIVE"
        return "UNKNOWN"

    def evaluate(self, cpu: int, utilization: float) -> CpuAlert | None:
        if cpu == self.reserved_cpu:
            return None
        utilization = max(0.0, min(float(utilization), 100.0))
        if utilization >= self.CRITICAL:
            severity = "CRITICAL"
        elif utilization >= self.WARNING:
            severity = "WARNING"
        else:
            return None
        alert = CpuAlert(cpu=cpu, utilization=utilization, severity=severity)
        for callback in tuple(self._callbacks):
            callback(alert)
        return alert


def read_cpu_times() -> dict[int, tuple[int, int]]:
    """Return ``cpu -> (busy, total)`` counters from /proc/stat."""
    result: dict[int, tuple[int, int]] = {}
    try:
        text = Path("/proc/stat").read_text()
    except OSError:
        return result
    for line in text.splitlines():
        fields = line.split()
        if not fields or not fields[0].startswith("cpu") or fields[0] == "cpu":
            continue
        try:
            cpu = int(fields[0][3:])
            values = [int(v) for v in fields[1:]]
        except (ValueError, IndexError):
            continue
        idle = values[3] + (values[4] if len(values) > 4 else 0)
        total = sum(values)
        result[cpu] = (total - idle, total)
    return result


def sample_utilization(interval: float = 1.0) -> dict[int, float]:
    """Measure per-CPU utilization over one interval."""
    before = read_cpu_times()
    time.sleep(max(0.0, interval))
    after = read_cpu_times()
    result: dict[int, float] = {}
    for cpu, (busy1, total1) in before.items():
        busy2, total2 = after.get(cpu, (busy1, total1))
        dt = total2 - total1
        result[cpu] = round(((busy2 - busy1) / dt) * 100.0, 1) if dt > 0 else 0.0
    return result
