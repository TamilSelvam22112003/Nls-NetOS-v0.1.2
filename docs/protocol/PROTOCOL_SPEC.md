# NLS Protocol Specification — Draft 0.1.2

**Status: NOT FROZEN.** Requirements skeleton only; not a wire specification or interoperable implementation.

## Purpose
Explore network-layer security for authenticated router relationships and protected packet transport. No claim is made that it improves on IPsec or TLS.

## Required wire-level decisions
- Versioning, framing, encoding/canonicalization and message bounds.
- Message types, required fields, length limits, unknown-field rules.
- Peer discovery and authenticated identity binding.
- Handshake state machine, transcript integrity, timers and retransmission.
- Cryptographic suite, key schedule/separation, AEAD nonce and rekey.
- Session IDs, counters, replay window and restart persistence.
- Errors, fail-closed behavior, rate limits and anti-amplification.
- Routing metadata, MTU/fragmentation, ICMP, NAT and forwarding integration.
- Certificate lifecycle, revocation, policy and trust-store updates.
- Downgrade protection, deprecation and interoperability.

## Security invariants
1. Unauthenticated peer data is not trusted identity or routing state.
2. No plaintext is released before record authentication succeeds.
3. An AEAD nonce is never reused with the same key.
4. Keys are separated by direction and purpose.
5. Replay rejection does not corrupt trusted session state.
6. Protocol failures never trigger automatic plaintext fallback.
7. Lengths, counters, queues, handshakes and retries have resource bounds.
8. Secrets are not written to logs or ordinary tables.

## Interoperability and change control
No interoperability is claimed. Test vectors and at least two independent implementations are required before treating the wire protocol as stable. Any handshake/header/crypto/identity/replay/downgrade change must update the spec, vectors and security analysis.
