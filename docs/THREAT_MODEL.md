# Threat Model (Initial Draft)

**Status:** incomplete; must be reviewed before implementation claims or deployment.

## Assets to protect

- Confidentiality and integrity of protected payloads.
- Authentication of peer routers and, where applicable, endpoint identity.
- Session keys, private keys, credentials, and trust configuration.
- Replay windows, counters, and session state.
- Routing and adjacency integrity.
- Availability and bounded resource consumption.
- Audit and operational state.

## Adversary capabilities considered

The initial design should assume an adversary can observe, inject, modify, replay, delay, reorder, duplicate, truncate, and drop network packets; send malformed or oversized input; spoof unauthenticated outer headers; trigger reconnection and rekey paths; and cause resource pressure. Compromised peers and compromised hosts are separate threat cases.

## Security objectives

- Mutual peer authentication where configured.
- Confidentiality and integrity for authenticated protected payloads.
- Strong binding of handshake transcript, peer identities, negotiated parameters, and session keys.
- Replay resistance across reordering, packet loss, restart, and rekey transitions.
- Downgrade resistance and strict version/cipher policy.
- Revocation and expiry enforcement.
- Bounded parser/handshake costs and explicit rate limits.
- Minimization—but not an unqualified claim of elimination—of traffic metadata leakage.

## Out of scope unless later added

Physical compromise, compromised trusted endpoints, global traffic analysis, endpoint malware, and availability against an adversary with enough capacity to saturate all upstream links cannot be solved solely by a transport protocol.

## Open questions

- Is the security association router-to-router, host-to-host, or both?
- What precise metadata may be visible to intermediate networks?
- How are keys bootstrapped and trust anchors provisioned?
- What is the recovery policy when a router restarts or loses persistent replay state?
- How does the design coexist with IPv4/IPv6, NAT, ECMP, PMTU, ICMP, and routing convergence?
- What are the handshake amplification and denial-of-service bounds?
- Which credential formats, rotation intervals, and revocation semantics are required?

## Required validation

Threat-model review, protocol state-machine analysis, parser fuzzing, cryptographic review, multi-router lab tests, and independent security assessment are prerequisites for any production deployment.
