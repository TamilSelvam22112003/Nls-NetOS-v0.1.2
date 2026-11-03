# NetOS v0.1.0 — boot-time onboarding prototype

## Architecture

```text
Boot -> Identity -> DTLS mutual authentication -> Validator
                                      |
                                      +-> Controller/Manager addresses
                                                  |
                                                  v
                                      Controller/Manager -> Config
                                                  |
                                                  v
                                               Running
```

## State machine

`Init -> Enroll (optional) -> ValidatorHandshake -> DiscoverControllers -> ControllerConnect -> FetchConfig -> Running`.
Any operational failure transitions to `Backoff`; retries use exponential backoff, jitter and port hopping across 12346/12347/12348.

The validator sends a 32-byte nonce. The router signs SHA-256(nonce) using RSA-PSS with its private key and returns the signature, serial, chassis and board-ID certificate. The server certificate chain is verified against `certs/root-ca.pem` and its `O` field is compared with `organization_name`.

## Mock validator

The runnable fake validator is `test/mock_validator/server.go`. It creates a root CA and server certificate at startup, sends challenges, validates the board certificate/serial/signature and returns controller/manager addresses. A small test or Go program can instantiate `mock_validator.New("Example Router Org")` and call `Start(ctx)`.

## Build and test

```sh
export NETOS_IDENTITY_PASSPHRASE='test-only-passphrase'
go test ./...
go build ./cmd/router
```

## Test certificate material

`certs/root-ca.pem` and `certs/device-boardid.pem` are test fixtures only. The matching test private key is intentionally not stored as a plaintext repository file. The encrypted-key fixture is a documented placeholder: `AESGCM:<base64(salt||nonce||ciphertext)>`, using scrypt N=32768, r=8, p=1 and AES-256-GCM. For a local test fixture, generate the key with `FileStore.Save`.

## Security warning

This is a prototype. Do not deploy the included certificate fixtures or passphrases in production. Replace FileStore with a real TPM-backed implementation before production use.

## Cisco interoperability

**Cisco interoperability is not supported.** This project uses a self-contained proprietary onboarding wire format and does not implement Cisco proprietary wire protocols or management interfaces.
