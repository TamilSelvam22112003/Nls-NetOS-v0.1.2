# NLS development environment

## Supported hosts

Bootstrap targets Ubuntu 20.04, 22.04 and 24.04. Python 3.10+ is required. Ubuntu 20.04 may need a separately provisioned newer Python; the installer does not replace system Python.

## Install

```bash
chmod +x scripts/dev-setup.sh scripts/install/*.sh scripts/verify-environment.sh
./scripts/dev-setup.sh
```

The bootstrap installs Ubuntu packages, FRRouting and a project-local Python virtual environment. It does not change host firewall policy, enable IP forwarding, or start FRR automatically.

## FRRouting

The installer installs `frr` and `frr-pythontools`, configures Zebra, OSPFv2, OSPFv3 and staticd, and enables the systemd unit. Review configuration before starting:

```bash
sudoedit /etc/frr/daemons
sudoedit /etc/frr/frr.conf
sudo systemctl start frr
sudo systemctl status frr
sudo vtysh -c 'show version'
sudo vtysh -c 'show daemons'
```

Do not start routing daemons on a production or connected network until interfaces, router IDs, authentication, route filters and firewall rules have been reviewed.

## Python development

```bash
source .venv/bin/activate
python -m pytest
ruff check usr/lib/nls tests
mypy usr/lib/nls
```

Docker, Mininet and Wireshark GUI are optional lab dependencies and are not installed automatically. Install them using official project instructions.

Run privileged networking tests only in disposable VMs or isolated lab networks. Never commit private keys, certificates, production databases, sensitive packet captures or runtime state.
