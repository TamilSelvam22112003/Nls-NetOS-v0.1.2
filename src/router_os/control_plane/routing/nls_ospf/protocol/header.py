"""Logical NLS header used by the NLS-OSPF carrier."""

from dataclasses import dataclass

from .constants import FLAG_AUTHENTICATED, FLAG_ENCRYPTED, NLS_HEADER_LENGTH_WORDS, NLS_VERSION


class NLSHeaderError(ValueError):
    """Raised when an NLS header violates the logical contract."""


@dataclass(frozen=True, slots=True)
class NLSHeader:
    version: int = NLS_VERSION
    header_length_words: int = NLS_HEADER_LENGTH_WORDS
    packet_type: int = 0
    flags: int = 0
    total_length: int = 0
    reserved: int = 0
    context_id: int = 0
    transaction_id: int = 0

    @property
    def header_length(self) -> int:
        return self.header_length_words * 4

    @property
    def encrypted(self) -> bool:
        return bool(self.flags & FLAG_ENCRYPTED)

    @property
    def authenticated(self) -> bool:
        return bool(self.flags & FLAG_AUTHENTICATED)

    def validate(self, body_length: int | None = None) -> None:
        if self.version != NLS_VERSION:
            raise NLSHeaderError(f"unsupported NLS version: 0x{self.version:02x}")
        if self.header_length_words != NLS_HEADER_LENGTH_WORDS:
            raise NLSHeaderError("NLS-OSPF requires HLen=5 in the supplied design")
        if not 0 <= self.packet_type <= 0xFF:
            raise NLSHeaderError("packet_type must fit in one byte")
        if not 0 <= self.flags <= 0xFF:
            raise NLSHeaderError("flags must fit in one byte")
        if not 0 <= self.total_length <= 0xFFFF:
            raise NLSHeaderError("total_length must fit in two bytes")
        if not 0 <= self.context_id <= 0xFFFFFFFF:
            raise NLSHeaderError("context_id must fit in four bytes")
        if not 0 <= self.transaction_id <= 0xFFFFFFFF:
            raise NLSHeaderError("transaction_id must fit in four bytes")
        if body_length is not None and self.total_length != self.header_length + body_length:
            raise NLSHeaderError(
                f"total_length={self.total_length} does not equal "
                f"header={self.header_length}+body={body_length}"
            )

    def with_body_length(self, body_length: int) -> "NLSHeader":
        header = NLSHeader(
            version=self.version,
            header_length_words=self.header_length_words,
            packet_type=self.packet_type,
            flags=self.flags,
            total_length=self.header_length + body_length,
            reserved=self.reserved,
            context_id=self.context_id,
            transaction_id=self.transaction_id,
        )
        header.validate(body_length)
        return header
