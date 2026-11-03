# NLS NetOS

This repository defines the source layout and configuration contract for the NLS router operating system.

## Layout status

- `etc/nls/`: starter YAML configuration with conservative defaults.
- `usr/lib/nls/`: Python package skeleton; modules are scaffolding, not a complete implementation.
- `etc/systemd/system/`: service unit templates; validate paths/users before enabling.
- `etc/frr/`: FRR configuration templates.
- `boot/`: build-time boot assets; kernel and initramfs must be generated for the target platform.
- `var/`, `run/`, `proc/`, `sys/`, `dev/`: runtime-managed data or virtual filesystems; placeholders document mount/state intent only.

## Security boundary

Do not commit private keys, live certificates, database files, session state, replay counters, generated logs, or credentials. Generate identity and key material on the target router with restrictive permissions. Treat configuration templates as untrusted until validated against the implementation.

## Current maturity

This commit establishes the requested filesystem-oriented layout. It does not claim that NLS services, packet processing, OSPF integration, or a bootable operating-system image are implemented.
