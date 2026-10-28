# Contributing

## Workflow

1. Start from an updated branch and open focused pull requests.
2. For protocol changes, update the specification and security considerations before implementation.
3. Add positive, negative, malformed-input, and regression tests.
4. Run `pytest` and `ruff check .` before submitting.
5. Explain limitations and threat assumptions in the pull request.

## Design rules

- Preserve a clean boundary between control and data planes.
- Treat packets and peer-controlled input as untrusted.
- Make state transitions explicit and observable.
- Use transactions for persistent state and define concurrency behavior.
- Prefer established cryptographic implementations.
- Version wire-format changes and test compatibility.
- Do not add privileged host-network operations without rollback and tests.

Include motivation, design, test evidence, security implications, migrations, and known gaps. Never describe a scaffold or mock as a completed protocol feature.
