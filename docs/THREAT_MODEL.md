# Threat Model (Initial Draft)

**Status:** incomplete; review is required before deployment.

## Assets
- Payload confidentiality and integrity.
- Peer router identity and trust configuration.
- Session/private keys and credentials.
- Replay windows, counters, and session state.
- Routing/adjacency integrity, availability, and audit state.

## Adversary capabilities
Assume an adversary can observe, inject, modify, replay, delay, reorder, duplicate, truncate, and drop traffic; send malformed/oversized inputs; spoof unauthenticated outer headers; trigger reconnect/rekey; and pressure resources. Compromised peers and endpoints are distinct cases.

## Objectives
- Mutual peer authentication where configured.
- Confidentiality and integrity for authenticated payloads.
- Bind handshake transcript, identities, negotiated parameters, and keys.
- Resist replay across reordering, packet loss, restart, and rekey.
- Resist downgrade and enforce strict version/suite policy.
- Enforce revocation/expiry.
- Bound parser and handshake work with explicit rate limits.
- Minimize, but do not claim to eliminate, traffic metadata leakage.

## Non-goals unless added
Physical compromise, compromised trusted endpoints, global traffic analysis, endpoint malware, and denial of service that saturates upstream capacity cannot be solved solely by a transport protocol.

## Open questions
- Router-to-router, host-to-host, or both?
- Which metadata is visible to intermediate networks?
- How are keys bootstrapped and trust anchors provisioned?
- What happens if restart loses persistent replay state?
- How does it coexist with IPv4/IPv6, NAT, ECMP, PMTU, ICMP and routing convergence?
- What are handshake amplification/DoS bounds?
- What credential formats, rotation, and revocation semantics apply?

## Required validation
Threat-model review, state-machine analysis, parser fuzzing, cryptographic review, multi-router lab testing, and independent security assessment are prerequisites for deployment.
