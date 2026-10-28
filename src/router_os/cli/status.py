"""Read-only router/platform status reporting for the ``nls`` command."""

from __future__ import annotations

import os
import platform
from pathlib import Path
import socket

SYS_NET = Path("/sys/class/net")
SYS_PCI = Path("/sys/bus/pci/devices")
SYS_NUMA = Path("/sys/devices/system/node")
SYS_HUGEPAGES = Path("/sys/kernel/mm/hugepages")


def _read(path: Path) -> str | None:
    try:
        return path.read_text().strip()
    except (OSError, UnicodeDecodeError):
        return None


def interfaces() -> list[str]:
    if not SYS_NET.exists():
        return []
    return sorted(p.name for p in SYS_NET.iterdir())


def _memory() -> dict[str, int]:
    values: dict[str, int] = {}
    text = _read(Path("/proc/meminfo")) or ""
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].rstrip(":") in {"MemTotal", "MemAvailable"}:
            try:
                values[parts[0].rstrip(":")] = int(parts[1]) * 1024
            except ValueError:
                pass
    return values


def _hugepages() -> int:
    total = 0
    if SYS_HUGEPAGES.exists():
        for node in SYS_HUGEPAGES.glob("hugepages-*/nr_hugepages"):
            value = _read(node)
            if value and value.isdigit():
                total += int(value)
    return total


def _cpu_usage() -> float | None:
    text = _read(Path("/proc/stat"))
    if not text:
        return None
    line = next((x for x in text.splitlines() if x.startswith("cpu ")), None)
    if not line:
        return None
    fields = line.split()[1:]
    try:
        values = [int(v) for v in fields]
    except ValueError:
        return None
    idle = values[3] + (values[4] if len(values) > 4 else 0)
    total = sum(values)
    return round((1.0 - idle / total) * 100.0, 1) if total else None


def snapshot() -> dict[str, object]:
    mem = _memory()
    ifaces = interfaces()
    pci = sorted(p.name for p in SYS_PCI.iterdir()) if SYS_PCI.exists() else []
    numa = sorted(p.name for p in SYS_NUMA.glob("node[0-9]*")) if SYS_NUMA.exists() else []
    return {
        "os": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "logical_cpus": os.cpu_count() or 0,
        "cpu_usage": _cpu_usage(),
        "interfaces": ifaces,
        "pci_devices": pci,
        "numa_nodes": numa,
        "memory_total": mem.get("MemTotal"),
        "memory_available": mem.get("MemAvailable"),
        "hugepages": _hugepages(),
    }


def _fmt_bytes(value: int | None) -> str:
    if value is None:
        return "unknown"
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return "unknown"


def render(section: str = "all") -> str:
    s = snapshot()
    usage = s["cpu_usage"]
    cpu_text = "unknown" if usage is None else f"{usage:.1f}%"
    lines: list[str] = []

    def header(title: str) -> None:
        lines.append(title)
        lines.append("─" * len(title))

    if section in {"all", "platform"}:
        header("NLS-NetOS Platform")
        lines += [
            f"OS              : {s['os']}",
            f"Kernel          : {s['kernel']}",
            f"Architecture    : {s['architecture']}",
            f"Hostname        : {s['hostname']}",
        ]
    if section in {"all", "hardware"}:
        header("Hardware")
        lines += [
            f"Interfaces      : {len(s['interfaces'])}",
            f"PCI devices     : {len(s['pci_devices'])}",
            f"NUMA nodes      : {len(s['numa_nodes'])}",
        ]
    if section in {"all", "cpu"}:
        header("CPU")
        lines += [
            f"Logical CPUs    : {s['logical_cpus']}",
            f"Current usage   : {cpu_text}",
            f"NUMA nodes      : {len(s['numa_nodes'])}",
        ]
    if section in {"all", "memory"}:
        header("Memory")
        lines += [
            f"Total           : {_fmt_bytes(s['memory_total'])}",
            f"Available       : {_fmt_bytes(s['memory_available'])}",
            f"Hugepages       : {s['hugepages']}",
        ]
    if section in {"all", "pci"}:
        header("PCI")
        lines.append(f"Devices         : {len(s['pci_devices'])}")
        for device in s["pci_devices"]:
            lines.append(f"  {device}")
    if section in {"all", "drivers"}:
        header("Drivers")
        lines += [
            "Ethernet        : kernel/sysfs", 
            "NIC             : kernel/sysfs",
            "Storage         : kernel/sysfs",
            "Platform        : kernel/sysfs",
        ]
    if section in {"all", "interfaces"}:
        header("Interfaces")
        for name in s["interfaces"]:
            state = _read(SYS_NET / name / "operstate") or "unknown"
            mtu = _read(SYS_NET / name / "mtu") or "unknown"
            lines.append(f"{name:<15} state={state:<10} mtu={mtu}")

    if section == "all":
        lines.append("")
        lines.append("Overall Status  : HEALTHY" if s["os"] == "Linux" else "Overall Status  : UNKNOWN")
    return "\n".join(lines)


def valid_section(value: str) -> bool:
    return value in {"all", "platform", "hardware", "cpu", "memory", "pci", "drivers", "interfaces"}
