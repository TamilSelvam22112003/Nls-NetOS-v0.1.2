#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUDO=""
if [[ $EUID -ne 0 ]]; then SUDO="sudo"; fi
$SUDO bash "$ROOT/scripts/install/install-system-dependencies.sh"
$SUDO bash "$ROOT/scripts/install/install-frr.sh"
bash "$ROOT/scripts/install/install-python-dependencies.sh"
bash "$ROOT/scripts/install/install-development-tools.sh"
cat <<'EOF'
NLS development bootstrap completed.
Review /etc/frr/daemons and /etc/frr/frr.conf before starting FRR.
Start manually: sudo systemctl start frr
Verify: make check
Test: make test
This script does not enable IP forwarding, alter firewall rules, or start routing daemons.
EOF
