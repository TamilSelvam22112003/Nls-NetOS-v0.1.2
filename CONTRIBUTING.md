# Contributing

## Workflow

1. Start from an updated branch and open focused pull requests.
2. For protocol changes, update the specification and security considerations before implementation.
3. Add positive, negative, malformed-input, and regression tests.
4. Run `pytest` and `ruff check .` before submitting.
5. Explain remaining limitations and threat assumptions in the pull request.

## Design rules

- Preserve a clean boundary between control plane and data plane.
- Treat all packet and peer-controlled input as untrusted.
- Make state transitions explicit and observable.
- Use transactions for persistent state and define concurrency behavior.
- Prefer standard libraries and established cryptographic implementations.
- Do not silently change wire formats; version them and test compatibility.
- Do not add root-level or host-network-changing behavior without documented rollback and tests.

## Pull requests

Include the motivation, design, test evidence, security implications, migration impact, and known gaps. Never describe a scaffold or mock as a completed protocol feature.
