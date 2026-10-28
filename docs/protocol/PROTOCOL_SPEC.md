# NLS Protocol Specification — Draft 0.1.2

**Status: NOT FROZEN.** This is a requirements skeleton, not a wire-level specification and not an interoperable protocol implementation.

## 1. Purpose

Explore a network-layer security protocol for authenticated router relationships and protected packet transport. NLS-NetOS is a research effort; this draft makes no claim that it improves on IPsec or TLS.

## 2. Requirements before a wire format is implemented

The specification must define:
- protocol versioning, framing, encoding, and canonicalization;
- message types, required fields, length bounds, and unknown-field handling;
- peer discovery and authenticated identity binding;
- handshake state machine, transcript integrity, timeouts, and retransmission;
- cryptographic suite, key schedule, key separation, AEAD nonce construction, and rekeying;
- session identifiers, packet counters, replay-window behavior, and restart persistence;
- error codes, fail-closed behavior, rate limits, and anti-amplification measures;
- routing metadata semantics, MTU/fragmentation, ICMP, NAT, and forwarding integration;
- certificate lifecycle, revocation, policy, and trust-store updates;
- downgrade protection, algorithm deprecation, and interoperability rules.

## 3. Security invariants

1. No unauthenticated peer-controlled data may be treated as trusted identity or routing state.
2. No plaintext is released until record authentication succeeds.
3. A nonce must never be reused with the same AEAD key.
4. Session keys must be separated by direction and purpose.
5. A replay rejection must not advance trusted session state incorrectly.
6. Protocol/version/authentication failures must not trigger automatic plaintext fallback.
7. Every length, counter, queue, handshake, and retry path must have bounded resources.
8. Secret key material must not be written to logs or ordinary application tables.

## 4. Interoperability

No interoperability is claimed at this stage. Test vectors and at least two independent implementations are required before the wire protocol can be treated as stable.

## 5. Change control

Any change to the handshake, packet header, cryptographic suite, identity binding, replay handling, or downgrade behavior must update this specification, test vectors, and security analysis before implementation is merged.
