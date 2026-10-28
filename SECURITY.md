# Security Policy

## Status

NLS-NetOS v0.1.2 is an experimental research scaffold, not a production security product. The current repository does not establish that an NLS protocol implementation is safe for deployment.

## Reporting vulnerabilities

Please do not publish exploit details for an unpatched, network-reachable issue in a public issue. Contact the maintainers through a private GitHub security advisory if that feature is enabled for this repository; otherwise contact the repository owner privately before public disclosure. Include affected commit, configuration, reproduction steps, impact, and logs with secrets removed.

## Security development requirements

- Never commit private keys, tokens, credentials, production packet captures, or customer data.
- Never implement custom cipher primitives.
- Do not disable certificate validation or authentication to make tests pass.
- Reject malformed, unauthenticated, unsupported, expired, or replayed protocol messages.
- Keep cryptographic APIs narrow and document nonce, key, and algorithm constraints.
- Require security review before enabling privileged packet processing or network configuration.
- Avoid claiming production readiness until independent review and interoperability testing are complete.
