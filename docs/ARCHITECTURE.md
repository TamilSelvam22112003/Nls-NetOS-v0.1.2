# Architecture

## Boundaries
1. **Boot/platform:** hardware and capability discovery; no protocol policy.
2. **Control plane:** peer relationships, trust, topology/LSDB state, routing decisions.
3. **Security services:** authentication, key agreement/derivation, AEAD, credential validation, replay protection, rotation, erasure.
4. **Data plane:** packet validation, classification, encapsulation/decapsulation, forwarding.
5. **Router-CA:** router identity and trust material with revocation/lifecycle semantics.
6. **Persistence:** non-secret control state via migrations and transactions; private keys belong in protected storage.
7. **Management:** configuration, health, diagnostics, and audit without secret exposure.

## Intended data flow (not implemented)
1. Discover a peer using a specified mechanism.
2. Validate peer identity and status against configured trust policy.
3. Run a versioned authenticated handshake.
4. Derive directionally separated traffic keys using a reviewed key schedule.
5. Authenticate and validate records before releasing plaintext.
6. Update replay state and packet counters atomically.
7. Invalidate state and erase secrets where feasible on failure, revocation, rekey, or shutdown.

## Data-plane safety
- Treat all packets and outer headers as attacker-controlled until validated.
- Bound parsing, allocations, queues, and cryptographic work.
- Authenticate associated routing/session fields before trusting them.
- Specify outer/inner address semantics and metadata leakage.
- Define MTU, fragmentation, ICMP, and malformed traffic handling.
- Never silently route failed protected traffic as plaintext.

## Persistence
Use SQLite and explicit transactions with versioned migrations initially. Planned entities include peer trust, neighbors, adjacencies, link-state records, virtual identity allocation, key/session metadata, and audit records. Never store traffic/private keys in plaintext tables.

## Integrations and failures
Initially integrate OSPF through an adapter to an established routing daemon rather than silently reimplementing it. IPsec/TLS areas are for comparison/interoperability tests, not home-grown replacements. Persistence errors, stale trust, invalid signatures, replay, exhausted counters, and expired sessions require explicit, bounded and observable failure transitions.
