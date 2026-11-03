#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
failed=0
for tool in python3 git gcc make ip vtysh zebra ospfd ospf6d openssl sqlite3 tcpdump; do
 if command -v "$tool" >/dev/null 2>&1; then echo "OK   $tool"; else echo "MISS $tool"; failed=1; fi
done
if [[ -x "$ROOT/.venv/bin/python" ]]; then "$ROOT/.venv/bin/python" -c 'import cryptography, yaml, scapy, psutil, pyroute2, pytest; print("OK   Python development packages")'; else echo "MISS .venv; run scripts/dev-setup.sh"; failed=1; fi
[[ -f /etc/frr/daemons ]] && echo "OK   /etc/frr/daemons" || { echo "MISS /etc/frr/daemons"; failed=1; }
exit "$failed"
