# 09 — Runtime Bootstrap

Status: Implemented prototype v0.1.2.

## Scope

This document records the implemented bootstrap foundation only. It does not claim that NLS-OSPF, packet forwarding, Router-CA enrollment, key generation, or database persistence are implemented.

## Startup contract

`python -m router_os` loads the validated router configuration and initializes the platform, cryptographic service boundary, control-plane boundary, and data-plane boundary in that order.

The repository-level `boot/router_boot.py` is a thin development entry point. Lifecycle logic is kept in `src/router_os/application.py` so installed Python execution does not depend on the repository working directory.

## Configuration

The bootstrap configuration is YAML and is loaded only by `router_os.config.loader`. Consumers receive the typed `NetOSConfig` model and must not parse YAML directly.

Configuration validation is strict for the v0.1.2 bootstrap schema: unsupported keys, invalid router IDs, invalid interface roles, missing fields, and duplicate interface names fail startup.

## Security boundary

The bootstrap crypto subsystem is lifecycle-only. It does not generate, persist, export, or log cryptographic secrets. Key generation and secure storage remain governed by the security architecture and are not falsely marked implemented by this milestone.

## Readiness

`READY` in this prototype means the configured runtime boundaries initialized successfully. It is not equivalent to the architecture document's operational/data-plane readiness, because NLS-OSPF, Router-CA synchronization, route calculation, RIB/FIB installation, and forwarding readiness are not implemented yet.
