# Security Policy

NLS-NetOS v0.1.2 is an experimental research scaffold, not a production security product. The repository does not establish that an NLS implementation is safe for deployment.

## Reporting vulnerabilities

Do not publish exploit details for an unpatched, network-reachable issue in a public issue. Contact the maintainers through a private GitHub security advisory if enabled; otherwise contact the repository owner privately before public disclosure. Include the affected commit, configuration, reproduction steps, impact, and logs with secrets removed.

## Security requirements

- Never commit private keys, tokens, credentials, sensitive packet captures, or customer data.
- Never implement custom cipher primitives.
- Do not disable certificate validation or authentication to make tests pass.
- Reject malformed, unauthenticated, unsupported, expired, or replayed messages.
- Document nonce, key, and algorithm constraints.
- Require security review before privileged packet processing or network configuration.
- Do not claim production readiness before independent review and interoperability testing.
