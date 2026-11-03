"""NLS-OSPF dataplane carrier classification and processing contracts."""

from dataclasses import dataclass
from enum import Enum

from router_os.control_plane.routing.nls_ospf.protocol.constants import PTYPE_OSPF_CARRIER
from router_os.control_plane.routing.nls_ospf.protocol.header import NLSHeader


class CarrierAction(str, Enum):
    DROP = "drop"
    DELIVER_OSPF = "deliver-ospf"
    ESTABLISHMENT = "establishment"


@dataclass(frozen=True, slots=True)
class SessionContext:
    context_id: int
    peer_router_id: int
    key_handle: str
    established: bool = True


class SessionTable:
    """In-memory dataplane session table keyed by NLS Context ID."""

    def __init__(self) -> None:
        self._sessions: dict[int, SessionContext] = {}

    def install(self, session: SessionContext) -> None:
        if session.context_id == 0:
            raise ValueError("context 0 is reserved for pre-session traffic")
        self._sessions[session.context_id] = session

    def lookup(self, context_id: int) -> SessionContext | None:
        return self._sessions.get(context_id)

    def remove(self, context_id: int) -> None:
        self._sessions.pop(context_id, None)


class NLSOSPFCarrier:
    """Classify an already parsed NLS packet without touching the LSDB."""

    def __init__(self, sessions: SessionTable) -> None:
        self._sessions = sessions

    def classify(self, header: NLSHeader) -> CarrierAction:
        if header.packet_type != PTYPE_OSPF_CARRIER:
            return CarrierAction.ESTABLISHMENT
        if header.context_id == 0 or not header.encrypted or not header.authenticated:
            return CarrierAction.DROP
        if self._sessions.lookup(header.context_id) is None:
            return CarrierAction.DROP
        return CarrierAction.DELIVER_OSPF
