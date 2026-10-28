"""Ethernet driver-facing abstraction.

This module intentionally avoids device-specific register access. Kernel NIC
support remains the hardware driver; NetOS consumes a stable interface model.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class EthernetPort:
    name: str
    mac: str | None = None
    mtu: int | None = None


def port(name, mac=None, mtu=None):
    return EthernetPort(name=name, mac=mac, mtu=mtu)
