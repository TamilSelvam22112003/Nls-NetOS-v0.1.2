# NLS-NetOS v0.1.2

**NLS-NetOS** is an experimental network operating-system and protocol research project exploring a new Layer 3 security architecture. It investigates router peer authentication, protected packet transport, key lifecycle management, router trust, and policy-controlled forwarding.

> **Status: scaffold / research prototype.** This repository does not yet provide a production-ready Internet security protocol. Do not deploy it on public networks or treat it as a replacement for IPsec, TLS, or other established protections. Wire formats, cryptography, threat model, interoperability, and failure behavior require specification, independent review, and testing before operational use.

## Principles
- Specification before implementation: versioned wire formats, state machines, downgrade rules, and security invariants.
- Use standard cryptographic primitives; do not invent cipher algorithms.
- Fail closed on invalid authentication, malformed messages, replay, expired credentials, and unsupported versions.
- Keep control plane, data plane, trust, persistence, and management independently testable.
- Add negative, property, integration, and security regression tests with each implementation stage.

## Initial architecture
- `boot/`, `platform/`: startup and platform discovery boundaries.
- `src/router_os/control_plane/routing/nls/`: protocol, neighbor/adjacency, trust, LSDB, topology, VIP, daemon boundaries.
- `src/router_os/data_plane/`: packet parsing, classification, forwarding, encapsulation boundaries.
- `src/router_os/crypto/`: cryptographic interfaces and key lifecycle boundaries.
- `src/router_os/router_ca/`: router identity, certificates, trust and registry integration.
- `database/`: SQLite-first schema/migration boundaries; MySQL is a later adapter, not an initial requirement.
- `docs/`: threat model, protocol specification, architecture, decisions and plan.
- `tests/`: unit, negative, integration and security regression tests.

## Development environment
Recommended initial target: Python 3.11+ on Ubuntu 22.04/24.04. First milestone is a safe user-space prototype; privileged packet I/O, kernel integration, hardware fast paths, and installation changes come only after specification and security review.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
pytest
```

The scaffold has no privileged installer or host-network reconfiguration. Do not run network-facing code as root until threat review, permissions, and rollback-safe integration tests exist.

## Documentation
- [Development roadmap](docs/DEVELOPMENT_PLAN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Protocol specification status](docs/protocol/PROTOCOL_SPEC.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

NLS may explore differences from IPsec and TLS, but resemblance to established systems is not evidence of security. Claims must be scoped, documented, tested, and independently reviewed.