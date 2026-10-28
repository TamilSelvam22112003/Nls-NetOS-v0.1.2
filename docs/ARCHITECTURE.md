# Architecture

## Architectural boundaries

The intended system has distinct areas:

1. **Boot and platform:** discovers hardware and capabilities; should not own protocol policy.
2. **Control plane:** tracks peer relationships, authenticated trust, topology/LSDB state, and routing decisions.
3. **Security services:** exposes small interfaces for authentication, key agreement, key derivation, AEAD, credential validation, replay protection, rotation, and erasure.
4. **Data plane:** validates packets, classifies traffic, performs encapsulation/decapsulation, and forwards according to installed state.
5. **Router-CA:** manages router identity and trust material, with explicit revocation and lifecycle rules.
6. **Persistence:** stores non-secret control state and metadata using schema migrations and transactions. Private keys require a separate protected storage boundary.
7. **Management/operations:** configuration, health status, diagnostics, and audit events without exposing secret material.

## Data-flow concept (not yet implemented)

1. A router discovers a peer through an explicitly specified mechanism.
2. The peer's identity and status are validated against a configured trust policy.
3. A versioned handshake authenticates both parties and establishes session state.
4. A reviewed key schedule derives directionally separated traffic keys.
5. The data plane authenticates and validates each protected record before releasing plaintext.
6. Replay state and packet counters are updated atomically with respect to session processing.
7. Failure, revocation, rekey, or shutdown invalidates state and erases secrets where feasible.

Every step is a design target; this document does not assert that the sequence has been implemented.

## Data-plane safety

- Treat outer headers and all packet contents as attacker-controlled until validated.
- Bound parsing, allocations, queues, and cryptographic work.
- Authenticate associated routing/session fields before trusting them.
- Define outer/inner address semantics and metadata leakage explicitly.
- Handle MTU, fragmentation, ICMP, and malformed traffic intentionally.
- Never silently route failed protected traffic as plaintext.

## Persistence model

Initial development should use SQLite and explicit transactions, with versioned migrations. Planned logical entities include peer identity/trust, neighbors, adjacencies, link-state records, virtual identity allocation, key/session metadata, and audit records. Traffic keys and private keys must not be stored in ordinary tables as plaintext.

## External integrations

The OSPF implementation should initially integrate through a documented adapter to an established routing daemon rather than recreating OSPF without a separate protocol implementation plan. IPsec and TLS folders are for interoperability experiments and comparisons, not duplicate home-grown implementations.

## Failure domains

Control-plane failure must not corrupt the data plane's security state. Persistence errors, stale trust, unexpected protocol versions, invalid signatures, replay detection, exhausted counters, and expired sessions require explicit state transitions and observable, bounded error handling.
