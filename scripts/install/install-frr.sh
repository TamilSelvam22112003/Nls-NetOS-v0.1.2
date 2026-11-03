#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $EUID -ne 0 ]]; then echo "Run with sudo: sudo $0" >&2; exit 1; fi
. /etc/os-release
[[ $ID == ubuntu ]] || { echo "Ubuntu is required." >&2; exit 1; }
case "$VERSION_ID" in 20.04|22.04|24.04) ;; *) echo "Unsupported Ubuntu release: $VERSION_ID" >&2; exit 1 ;; esac
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y frr frr-pythontools
install -d -o frr -g frr -m 0750 /etc/frr
if [[ -f /etc/frr/daemons ]]; then cp -a /etc/frr/daemons "/etc/frr/daemons.nls-backup.$(date +%Y%m%d%H%M%S)"; fi
cat > /etc/frr/daemons <<'EOF'
zebra=yes
ospfd=yes
ospf6d=yes
staticd=yes
bfdd=no
fabricd=no
vrrpd=no
EOF
chown frr:frr /etc/frr/daemons
chmod 0640 /etc/frr/daemons
systemctl enable frr
echo "FRR installed and enabled. Review /etc/frr/daemons and /etc/frr/frr.conf before starting."
echo "Start manually when ready: sudo systemctl start frr"
