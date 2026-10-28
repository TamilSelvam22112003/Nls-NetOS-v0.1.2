"""Tests for CPU reservation and overload policy."""

from src.router_os.cpu_guard.manager import CpuGuard


def test_odd_cpu_count_reserves_one_cpu() -> None:
    guard = CpuGuard(5)
    assert guard.reserved_cpu == 4
    assert guard.state(4) == "NULL"
    assert guard.affinity_mask() == (0, 1, 2, 3)


def test_even_cpu_count_does_not_reserve_cpu() -> None:
    guard = CpuGuard(8)
    assert guard.reserved_cpu is None
    assert guard.affinity_mask() == tuple(range(8))


def test_warning_and_critical_alerts() -> None:
    guard = CpuGuard(5)
    assert guard.evaluate(0, 89.9) is None
    warning = guard.evaluate(0, 90.0)
    assert warning is not None
    assert warning.severity == "WARNING"
    critical = guard.evaluate(0, 100.0)
    assert critical is not None
    assert critical.severity == "CRITICAL"


def test_reserved_cpu_can_alert_but_stays_null() -> None:
    guard = CpuGuard(5)
    alert = guard.evaluate(4, 95.0)
    assert guard.state(4) == "NULL"
    assert alert is not None
    assert alert.responsibilities == ("LAN", "WAN", "Router-CA")
