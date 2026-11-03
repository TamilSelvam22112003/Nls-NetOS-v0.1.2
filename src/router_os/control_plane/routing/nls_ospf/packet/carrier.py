"""Logical OSPF payload carried by an established NLS session."""

from dataclasses import dataclass

from router_os.control_plane.routing.nls_ospf.protocol.constants import OSPF_DBD, OSPF_HELLO, OSPF_VERSION_2


class OSPFCarrierError(ValueError):
    """Raised when an OSPF carrier payload is invalid."""


@dataclass(frozen=True, slots=True)
class OSPFCommonHeader:
    version: int
    packet_type: int
    packet_length: int
    router_id: int
    area_id: int
    checksum: int = 0
    au_type: int = 0

    def validate(self, payload_length: int) -> None:
        if self.version != OSPF_VERSION_2:
            raise OSPFCarrierError(f"unsupported OSPF version: {self.version}")
        if self.packet_type not in (OSPF_HELLO, OSPF_DBD):
            raise OSPFCarrierError(f"unsupported OSPF carrier type: {self.packet_type}")
        if self.packet_length < 24:
            raise OSPFCarrierError("OSPF packet length is below the common header size")
        if self.packet_length != 24 + payload_length:
            raise OSPFCarrierError("OSPF packet length does not match carrier payload")


@dataclass(frozen=True, slots=True)
class OSPFHello:
    network_mask: int
    hello_interval: int
    options: int
    router_priority: int
    dead_interval: int
    designated_router: int
    backup_designated_router: int
    neighbors: tuple[int, ...] = ()


@dataclass(frozen=True, slots=True)
class OSPFDBD:
    interface_mtu: int
    options: int
    flags: int
    dd_sequence: int
    lsa_headers: bytes = b""
