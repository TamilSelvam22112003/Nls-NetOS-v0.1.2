"""NLS-OSPF packet constants for the prototype dataplane carrier."""

NLS_VERSION = 0x12
NLS_HEADER_LENGTH_WORDS = 5
NLS_HEADER_LENGTH_BYTES = NLS_HEADER_LENGTH_WORDS * 4
NLS_UDP_PORT = 9999

PTYPE_HELLO = 0x01
PTYPE_META_REQ = 0x02
PTYPE_META_RESP = 0x03
PTYPE_KEY_XCHG = 0x04
PTYPE_ACK = 0x05
PTYPE_OSPF_CARRIER = 0x06

FLAG_ENCRYPTED = 0x80
FLAG_AUTHENTICATED = 0x40
FLAG_KEY_MATERIAL = 0x20
FLAG_CONTROL = 0x10

OSPF_VERSION_2 = 2
OSPF_HELLO = 1
OSPF_DBD = 2

AEAD_TAG_LENGTH = 16
TRANSACTION_ID_BYTES = 4
CONTEXT_ID_BYTES = 4

# The supplied design declares a 20-byte NLS header. The currently enumerated
# fields account for 16 bytes, so byte-level NLS serialization is intentionally
# deferred until the missing four-byte field is specified.
WIRE_HEADER_LAYOUT_COMPLETE = False
