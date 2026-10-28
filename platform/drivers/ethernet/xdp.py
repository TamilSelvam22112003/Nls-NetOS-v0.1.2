"""XDP/AF_XDP integration boundary for Linux Ethernet ports."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import socket


@dataclass(frozen=True)
class XDPCapability:
    interface: str
    bpf_available: bool
    af_xdp_available: bool
    native_xdp: bool


def capability(interface: str) -> XDPCapability:
    bpf = Path("/sys/fs/bpf").is_dir() or Path("/proc/sys/kernel/unprivileged_bpf_disabled").exists()
    af_xdp = bpf and hasattr(socket, "AF_XDP")
    # Native XDP support is NIC/driver specific; sysfs alone cannot prove it.
    native = (Path("/sys/class/net") / interface / "xdp").exists()
    return XDPCapability(interface, bpf, af_xdp, native)


def validate(interface: str) -> XDPCapability:
    if not (Path("/sys/class/net") / interface).exists():
        raise FileNotFoundError(interface)
    return capability(interface)
