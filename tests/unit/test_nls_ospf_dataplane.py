"""Unit tests for the NLS-OSPF dataplane carrier contracts."""

from router_os.control_plane.routing.nls_ospf.packet.carrier import OSPFCommonHeader
from router_os.control_plane.routing.nls_ospf.protocol.constants import (
    FLAG_AUTHENTICATED,
    FLAG_ENCRYPTED,
    PTYPE_OSPF_CARRIER,
)
from router_os.control_plane.routing.nls_ospf.protocol.header import NLSHeader
from router_os.data_plane.nls_engine.anti_replay.window import ReplayWindow
from router_os.data_plane.nls_engine.carrier import (
    CarrierAction,
    NLSOSPFCarrier,
    SessionContext,
    SessionTable,
)


def test_established_encrypted_ospf_carrier_is_delivered() -> None:
    sessions = SessionTable()
    sessions.install(SessionContext(1, 0x01020304, "key-handle-1"))
    engine = NLSOSPFCarrier(sessions)
    header = NLSHeader(
        packet_type=PTYPE_OSPF_CARRIER,
        flags=FLAG_ENCRYPTED | FLAG_AUTHENTICATED,
        context_id=1,
        transaction_id=7,
        total_length=20,
    )
    assert engine.classify(header) == CarrierAction.DELIVER_OSPF


def test_unknown_context_is_dropped() -> None:
    engine = NLSOSPFCarrier(SessionTable())
    header = NLSHeader(
        packet_type=PTYPE_OSPF_CARRIER,
        flags=FLAG_ENCRYPTED | FLAG_AUTHENTICATED,
        context_id=9,
    )
    assert engine.classify(header) == CarrierAction.DROP


def test_replay_window_rejects_duplicate() -> None:
    window = ReplayWindow(4)
    assert window.accept(10)
    assert not window.accept(10)
    assert window.accept(11)


def test_ospf_common_header_length() -> None:
    header = OSPFCommonHeader(2, 1, 28, 0x01020304, 0, 0, 0)
    header.validate(4)
