# Decision 0001: Development Baseline

- **Status:** Accepted for initial scaffold
- **Date:** 2026-10-28

## Decisions
- Python 3.11+ for the first user-space prototype.
- SQLite with explicit transactions and schema migrations initially.
- Keep privileged packet processing and host changes out of the first scaffold.
- Prefer adapters to established routing daemons for lab integration.
- Wire format and cryptographic suite are unapproved until reviewed.
- Build test/CI gates before enabling network-facing behavior.

## Consequences
This enables testable iteration without prematurely committing to a database server, kernel datapath, or unreviewed wire format. Future decisions should document migration implications.
