"""Unit tests for the NLS-OSPF encrypted dataplane carrier."""

from router_os.data_plane.nls_engine.ospf_carrier import (
    CarrierError,
    FLAG_AUTHENTICATED,
    FLAG_ENCRYPTED,
    NLSHeader,
    NLSSession,
    SessionTable,
    open_ospf,
    protect_ospf,
)


def test_encrypt_decrypt_and_replay_reject() -> None:
    session = NLSSession(1, bytes(range(32)), 0x02020202)
    sessions = SessionTable()
    sessions.install(session)
    header = NLSHeader(0x12, 5, 0x06, FLAG_ENCRYPTED | FLAG_AUTHENTICATED, 0, 0, 1, 1, 0)
    packet = protect_ospf(session, header, b"OSPF-HELLO")
    decoded, payload = open_ospf(sessions, packet)
    assert decoded.context_id == 1
    assert payload == b"OSPF-HELLO"
    try:
        open_ospf(sessions, packet)
    except CarrierError as exc:
        assert "replayed" in str(exc)
    else:
        raise AssertionError("replayed packet was accepted")


def test_unknown_context_is_rejected() -> None:
    header = NLSHeader(0x12, 5, 0x06, FLAG_ENCRYPTED | FLAG_AUTHENTICATED, 20, 0, 99, 1, 0)
    try:
        open_ospf(SessionTable(), header.encode())
    except CarrierError as exc:
        assert "unknown NLS session" in str(exc)
    else:
        raise AssertionError("unknown context was accepted")
