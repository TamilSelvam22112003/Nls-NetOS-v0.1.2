# custom-router

Self-contained lab router onboarding implementation. It is **not Cisco interoperable**; Cisco SD-WAN/Validator/OMP wire formats are proprietary and are not implemented here.

## Architecture

```text
Boot -> Identity -> DTLS Validator/CA -> mutual authentication
                                      -> controller/manager discovery
                                      -> controller connect
                                      -> manager /config fetch
                                      -> atomic configuration activation
                                      -> Running
```

## State machine

```text
Init -> Enroll (optional) -> ValidatorHandshake -> DiscoverControllers
     -> ControllerConnect -> FetchConfig -> Running
                         -> Backoff -> exponential jitter + port hop -> retry
```

Every state transition is logged. Authentication failures close the DTLS connection before retry. Default retry ports are 12346, 12347 and 12348.

## Wire protocol

The lab handshake uses a length-prefixed TLV stream: 4-byte big-endian frame length, 2-byte message type, 4-byte value length, then JSON. The Validator sends a cryptographically random 32-byte nonce. The router returns an RSA-PSS/SHA-256 signature, serial, chassis and board-ID certificate. The Validator verifies certificate validity, serial authorization and signature, then returns controller/manager endpoints.

## Build and run

```bash
go build ./...
go test ./...
export CUSTOM_ROUTER_KEY_PASSPHRASE='lab-passphrase'
go run ./cmd/router
```

The lab manager is expected to expose `GET <manager>/config`. Controller and manager adapters use context-aware HTTP(S) calls.

## Mock Validator

`test/mock_validator/server.go` creates a real DTLS Validator test server with a generated root CA and server certificate, sends 256-bit challenges, verifies board certificate signatures and returns controller/manager endpoints. Tests cover success, organization mismatch, bad signature, expired/unknown identity and retry trigger behavior.

## Certificate fixtures

`certs/root-ca.pem` and `certs/device-boardid.pem` are real PEM public certificates. They are lab fixtures only. The matching unencrypted private key is deliberately not committed. `certs/device-boardid.key.enc` documents the FileStore record as `AESGCM:<base64 nonce>:<base64 ciphertext>` followed by the board certificate PEM. Generate a matching encrypted private key with `CUSTOM_ROUTER_KEY_PASSPHRASE` when provisioning the lab router.

## Security and compatibility warning

The FileStore is a lab persistence implementation; production hardware should use a TPM-backed identity, secure boot, protected flash/NVRAM, certificate revocation, secure time, anti-rollback and a hardened authenticated configuration channel.

**Cisco interoperability is not supported.** This repository implements a self-contained custom onboarding protocol and must not be represented as a Cisco SD-WAN client.
