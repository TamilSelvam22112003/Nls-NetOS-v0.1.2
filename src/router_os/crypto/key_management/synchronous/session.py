"""Synchronous NLS traffic-key primitives.

The synchronous key is secret key material. It is never exported as part of
an NLS packet. A neighbor-specific traffic key is derived from it instead.
"""
from __future__ import annotations

import hashlib
import hmac


def derive_neighbor_key(synchronous_key: bytes, local_router_id: int, peer_router_id: int, epoch: int) -> bytes:
    """Derive a deterministic 256-bit neighbor traffic key for one epoch."""
    if len(synchronous_key) < 32:
        raise ValueError("synchronous key must contain at least 32 bytes")
    context = (
        b"NLS-NETOS-SYNC-TRAFFIC-V1" +
        local_router_id.to_bytes(4, "big") +
        peer_router_id.to_bytes(4, "big") +
        epoch.to_bytes(8, "big")
    )
    return hmac.new(synchronous_key, context, hashlib.sha256).digest()
