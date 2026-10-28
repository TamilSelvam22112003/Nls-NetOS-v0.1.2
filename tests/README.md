# Testing strategy

- Unit: parsers, validators, state machines, policy and persistence adapters.
- Property: bounded parsing, serialization round trips, state invariants.
- Negative: truncation, excessive lengths, invalid versions/authentication, replay, stale trust, resource limits.
- Concurrency: session/key updates, replay windows, LSDB updates, migrations, revocation.
- Integration: isolated IPv4/IPv6 router lab and routing-daemon adapter.
- Security regression: malformed input and previously reported defects.
- Fuzzing and performance are separate gates; unit tests alone are not a security assessment.
