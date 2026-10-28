# Decision 0001: Development Baseline

- **Status:** Accepted for initial scaffold
- **Date:** 2026-10-28

## Decisions

- Python 3.11+ for the first user-space prototype.
- SQLite with explicit transactions and schema migrations for initial control-plane persistence.
- Keep data-plane packet processing and privileged host changes out of the initial scaffold.
- Prefer adapters to established routing daemons for lab integration.
- Treat protocol wire format and cryptographic suite as unapproved until documented review.
- Build test and CI gates before enabling network-facing behavior.

## Consequences

This baseline enables rapid, testable implementation without prematurely committing to a database server, kernel datapath, or unreviewed wire format. A later design record may change these choices with migration implications documented.
