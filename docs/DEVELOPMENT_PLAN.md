# Development Plan

This is a scaffold. Milestones are planned work, not claims that capabilities are complete.

## M0 — Repository foundation
Establish layout, coding conventions, CI, security reporting, platforms, and dependency policy. Keep privileged actions disabled.
**Acceptance:** fresh virtual-environment install; lint, type checks, tests in CI.

## M1 — Threat model and requirements
Identify assets, adversaries, trust boundaries, deployment assumptions, confidentiality/integrity, identity, metadata, replay, downgrade, and DoS objectives. Decide IP routing, NAT, MTU/fragmentation, ICMP and middlebox behavior.
**Acceptance:** reviewed threat model and requirements matrix.

## M2 — Wire format and state machines
Specify framing, version negotiation, encoding, message limits, handshake, timeouts, retries, replay windows, rekey, restart, key erasure, peer discovery, Router-CA trust, downgrade and fail-closed behavior.
**Acceptance:** reference vectors and malformed/truncated/oversized/unknown-field/version/replay tests.

## M3 — Cryptographic review
Select standard constructions after expert review; specify authentication, ephemeral agreement, transcript binding, derivation, nonce allocation, AEAD, key separation, algorithm deprecation.
**Acceptance:** documented rationale, vectors, negative crypto tests, independent review before deployment.

## M4 — User-space prototype
Implement pure data types/validators, explicit state machines and injected interfaces; add SQLite migrations for trust, LSDB, VIP and peer state.
**Acceptance:** unit/property, transaction/concurrency, crash/restart tests without privileged network I/O.

## M5 — Control-plane lab
Integrate routing through an adapter; specify control/data packet classification; test recovery, route changes, revocation, partial partitions.
**Acceptance:** reproducible multi-router lab with packet traces and negative cases.

## M6 — Data plane/hardening
Only implement after wire/state review. Define MTU/fragmentation/PMTU/ICMP, rate limits, resource caps, backpressure, privilege boundary, shutdown and rollback.
**Acceptance:** fuzz/load/abuse tests, baselines, failure injection and external review.

## M7 — Release
Create reproducible packages and checksums; document provisioning, upgrade/rollback, telemetry, incidents and support policy.
**Acceptance:** clean-VM install/upgrade/uninstall; signed artifacts; no production claims before independent review.
