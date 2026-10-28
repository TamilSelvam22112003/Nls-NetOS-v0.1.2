# Development Plan

## Status

This is the initial repository scaffold. Milestones below are planned work, not claims that those capabilities are implemented.

## M0 — Repository foundation

- Establish package layout, coding conventions, CI, and security reporting.
- Define supported development platforms and dependency policy.
- Keep privileged actions disabled.

**Acceptance:** clean installation in a fresh virtual environment; lint, type checks, and tests run in CI.

## M1 — Threat model and protocol requirements

- Identify assets, adversaries, trust boundaries, deployment assumptions, and non-goals.
- Define what NLS protects: confidentiality, integrity, peer identity, traffic metadata, replay, downgrade, and denial-of-service boundaries.
- Decide how NLS relates to IP routing, NAT, MTU/fragmentation, ICMP, and middleboxes.
- Record each design decision and rejected alternative.

**Acceptance:** a reviewed threat model and requirements matrix; no unqualified claims that source identity or metadata is hidden.

## M2 — Wire format and state machines

- Specify message framing, version negotiation, message limits, canonical encoding, error handling, handshake state machine, and session lifecycle.
- Define replay counters/windows, timeout rules, rekey behavior, restart behavior, and key erasure.
- Define authenticated peer discovery and Router-CA trust provisioning.
- Specify downgrade resistance and fail-closed behavior.

**Acceptance:** reference vectors and parser/validator tests for valid, malformed, truncated, oversized, unknown-field, invalid-version, and replayed inputs.

## M3 — Cryptographic design review

- Select standard constructions based on the threat model and expert review.
- Define authentication, ephemeral key agreement, transcript binding, key derivation, nonce allocation, AEAD usage, and key separation.
- Specify algorithm agility and deprecation policy without unsafe negotiation.
- Require independent review before network deployment.

**Acceptance:** documented cryptographic rationale; deterministic test vectors; negative tests including authentication failure, wrong keys, altered associated data, and nonce/state misuse.

## M4 — User-space core prototype

- Implement pure protocol data types and validation first.
- Add explicit state machines and dependency-injected interfaces.
- Add persistence for trust, LSDB, VIP, and peer state behind repository interfaces.
- Use SQLite with migrations for the first implementation; do not make a live MySQL service a prerequisite.

**Acceptance:** unit and property tests; transaction/concurrency tests; crash/restart tests; no privileged networking required.

## M5 — Control-plane and lab integration

- Integrate routing with a controlled lab and a documented routing-daemon boundary.
- Define how control packets are distinguished from protected data traffic.
- Validate failure recovery, route changes, peer revocation, and partial network partitions.

**Acceptance:** reproducible multi-router lab tests with packet traces, negative cases, and documented limitations.

## M6 — Data plane and operational hardening

- Implement packet processing only after wire-format and state-machine reviews.
- Define MTU, fragmentation, PMTU discovery, ICMP behavior, rate limits, resource caps, and backpressure.
- Add least-privilege execution, capability boundaries, safe startup/shutdown, observability, and rollback-safe configuration.

**Acceptance:** fuzzing, load and abuse tests, performance baselines, failure-injection tests, and external security review.

## M7 — Packaging and release

- Produce reproducible packages and checksums.
- Document configuration, key provisioning, upgrade/rollback, telemetry, and incident response.
- Publish compatibility and security support policy.

**Acceptance:** clean-VM installation/upgrade/uninstall tests and signed release artifacts. No production-readiness claim before independent security review.
