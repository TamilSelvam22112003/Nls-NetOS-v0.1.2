"""NLS-OSPF dataplane carrier: session lookup, replay protection and AEAD."""
from __future__ import annotations

from dataclasses import dataclass
import struct

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NLS_VERSION = 0x12
NLS_HEADER_BYTES = 20
PTYPE_OSPF_CARRIER = 0x06
FLAG_ENCRYPTED = 0x80
FLAG_AUTHENTICATED = 0x40


class CarrierError(ValueError):
    """Raised when an NLS-OSPF carrier packet is invalid."""


@dataclass(frozen=True, slots=True)
class NLSHeader:
    version: int
    hlen_words: int
    ptype: int
    flags: int
    total_length: int
    reserved: int
    context_id: int
    transaction_id: int
    extension: int = 0

    def validate(self, actual_length: int) -> None:
        if self.version != NLS_VERSION or self.hlen_words != 5:
            raise CarrierError("unsupported NLS version or header length")
        if self.ptype != PTYPE_OSPF_CARRIER:
            raise CarrierError("not an NLS-OSPF carrier packet")
        if not self.flags & FLAG_ENCRYPTED or not self.flags & FLAG_AUTHENTICATED:
            raise CarrierError("OSPF carrier requires encryption and authentication")
        if self.total_length != actual_length or self.total_length < NLS_HEADER_BYTES:
            raise CarrierError("invalid NLS total length")
        if self.context_id == 0:
            raise CarrierError("OSPF carrier requires an established context")

    def encode(self) -> bytes:
        return struct.pack(
            "!BBBBHHIII I",
            self.version, self.hlen_words, self.ptype, self.flags,
            self.total_length, self.reserved, self.context_id,
            self.transaction_id, self.extension,
        )

    @classmethod
    def decode(cls, data: bytes) -> "NLSHeader":
        if len(data) < NLS_HEADER_BYTES:
            raise CarrierError("truncated NLS header")
        return cls(*struct.unpack("!BBBBHHIII I", data[:NLS_HEADER_BYTES]))


@dataclass(slots=True)
class ReplayWindow:
    highest: int = -1
    width: int = 64
    bitmap: int = 0

    def accept(self, counter: int) -> bool:
        if counter < 0:
            return False
        if self.highest < 0:
            self.highest, self.bitmap = counter, 1
            return True
        if counter > self.highest:
            shift = counter - self.highest
            self.bitmap = 1 if shift >= self.width else ((self.bitmap << shift) | 1) & ((1 << self.width) - 1)
            self.highest = counter
            return True
        delta = self.highest - counter
        if delta >= self.width or (self.bitmap & (1 << delta)):
            return False
        self.bitmap |= 1 << delta
        return True


@dataclass(frozen=True, slots=True)
class NLSSession:
    context_id: int
    key: bytes
    peer_router_id: int
    algorithm: str = "AES-256-GCM"

    def __post_init__(self) -> None:
        if len(self.key) != 32:
            raise ValueError("NLS-OSPF AES-256-GCM session keys must be 32 bytes")
        if self.algorithm != "AES-256-GCM":
            raise ValueError("unsupported prototype AEAD algorithm")


class SessionTable:
    def __init__(self) -> None:
        self._sessions: dict[int, NLSSession] = {}
        self._replay: dict[int, ReplayWindow] = {}

    def install(self, session: NLSSession) -> None:
        if session.context_id == 0:
            raise ValueError("context 0 is reserved for pre-session traffic")
        self._sessions[session.context_id] = session
        self._replay.setdefault(session.context_id, ReplayWindow())

    def remove(self, context_id: int) -> None:
        self._sessions.pop(context_id, None)
        self._replay.pop(context_id, None)

    def lookup(self, context_id: int) -> NLSSession:
        try:
            return self._sessions[context_id]
        except KeyError as exc:
            raise CarrierError("unknown NLS session context") from exc

    def accept_counter(self, context_id: int, counter: int) -> bool:
        return self._replay[context_id].accept(counter)


def build_nonce(context_id: int, transaction_id: int) -> bytes:
    if not 0 <= context_id <= 0xFFFFFFFF or not 0 <= transaction_id <= 0xFFFFFFFFFFFFFFFF:
        raise ValueError("nonce components out of range")
    return struct.pack("!IQ", context_id, transaction_id)


def protect_ospf(session: NLSSession, header: NLSHeader, ospf_payload: bytes) -> bytes:
    if header.context_id != session.context_id:
        raise CarrierError("session/header context mismatch")
    nonce = build_nonce(header.context_id, header.transaction_id)
    # The header is authenticated as AAD; the AEAD tag remains outside it.
    provisional = NLSHeader(header.version, header.hlen_words, header.ptype,
                            header.flags, NLS_HEADER_BYTES + len(ospf_payload) + 16,
                            header.reserved, header.context_id, header.transaction_id,
                            header.extension)
    ciphertext = AESGCM(session.key).encrypt(nonce, ospf_payload, provisional.encode())
    return provisional.encode() + ciphertext


def open_ospf(table: SessionTable, packet: bytes) -> tuple[NLSHeader, bytes]:
    header = NLSHeader.decode(packet)
    header.validate(len(packet))
    session = table.lookup(header.context_id)
    if not table.accept_counter(header.context_id, header.transaction_id):
        raise CarrierError("replayed NLS-OSPF packet")
    nonce = build_nonce(header.context_id, header.transaction_id)
    try:
        plaintext = AESGCM(session.key).decrypt(nonce, packet[NLS_HEADER_BYTES:], header.encode())
    except Exception as exc:
        raise CarrierError("NLS-OSPF authentication/decryption failed") from exc
    return header, plaintext
