"""Minimal OSPFv2 payload codec used inside the NLS carrier."""
from __future__ import annotations

from dataclasses import dataclass
import ipaddress
import struct

OSPF_VERSION = 2
OSPF_HELLO = 1
OSPF_DBD = 2
OSPF_COMMON_HEADER = 24


class OSPFPayloadError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class OSPFHeader:
    packet_type: int
    packet_length: int
    router_id: int
    area_id: int
    checksum: int = 0
    auth_type: int = 0

    def encode(self) -> bytes:
        return struct.pack("!BBHIIHH8s", OSPF_VERSION, self.packet_type,
                           self.packet_length, self.router_id, self.area_id,
                           self.checksum, self.auth_type, b"\x00" * 8)

    @classmethod
    def decode(cls, data: bytes) -> "OSPFHeader":
        if len(data) < OSPF_COMMON_HEADER:
            raise OSPFPayloadError("truncated OSPF common header")
        version, ptype, plen, rid, area, checksum, auth_type, _ = struct.unpack(
            "!BBHIIHH8s", data[:OSPF_COMMON_HEADER]
        )
        if version != OSPF_VERSION:
            raise OSPFPayloadError("unsupported OSPF version")
        if plen < OSPF_COMMON_HEADER or plen > len(data):
            raise OSPFPayloadError("invalid OSPF packet length")
        return cls(ptype, plen, rid, area, checksum, auth_type)


@dataclass(frozen=True, slots=True)
class OSPFHello:
    network_mask: int
    hello_interval: int
    options: int
    router_priority: int
    dead_interval: int
    dr: int
    bdr: int
    neighbors: tuple[int, ...] = ()

    def encode(self) -> bytes:
        body = struct.pack("!IHB BIII", self.network_mask, self.hello_interval,
                           self.options, self.router_priority, self.dead_interval,
                           self.dr, self.bdr)
        body += b"".join(struct.pack("!I", n) for n in self.neighbors)
        return body


@dataclass(frozen=True, slots=True)
class OSPFDBD:
    interface_mtu: int
    options: int
    flags: int
    sequence: int
    lsa_headers: tuple[bytes, ...] = ()

    def encode(self) -> bytes:
        if any(len(h) != 20 for h in self.lsa_headers):
            raise OSPFPayloadError("LSA headers must be 20 bytes")
        return struct.pack("!HBBI", self.interface_mtu, self.options,
                           self.flags, self.sequence) + b"".join(self.lsa_headers)


def router_id(value: str) -> int:
    return int(ipaddress.IPv4Address(value))
