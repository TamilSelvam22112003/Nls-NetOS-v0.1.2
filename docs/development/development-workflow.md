# NLS development workflow

1. Clone the repository and run `./scripts/dev-setup.sh` on a supported Ubuntu VM.
2. Run `make check` and resolve missing dependencies.
3. Develop and test protocol modules without root privileges wherever possible.
4. Use isolated network namespaces, Mininet or VM topologies for packet-path and routing tests.
5. Start FRR only after reviewing daemon selection and routing policy.
6. Run `make test`, `make lint`, `make typecheck` and `make package` before submitting changes.
7. Validate privileged packet I/O, forwarding and firewall behavior in disposable VMs.

NLS services should communicate with FRR through a narrow adapter layer (VTYSH/FRR management interfaces), not by modifying FRR internals. Configuration generation must be deterministic and validated before application.
