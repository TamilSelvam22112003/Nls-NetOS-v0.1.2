#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $EUID -ne 0 ]]; then echo "Run with sudo: sudo $0" >&2; exit 1; fi
. /etc/os-release
if [[ $ID != ubuntu ]]; then echo "Supported host: Ubuntu 20.04, 22.04 or 24.04." >&2; exit 1; fi
case "$VERSION_ID" in 20.04|22.04|24.04) ;; *) echo "Unsupported Ubuntu release: $VERSION_ID" >&2; exit 1 ;; esac
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends ca-certificates curl wget git jq pkg-config build-essential gcc g++ make cmake ninja-build clang gdb python3 python3-dev python3-venv python3-pip libssl-dev libffi-dev libpcap-dev libsqlite3-dev libnl-3-dev libnl-route-3-dev libsystemd-dev iproute2 iputils-ping iputils-tracepath traceroute ethtool bridge-utils nftables iptables tcpdump socat dnsutils net-tools sqlite3 openssl linux-headers-generic shellcheck
 echo "NLS system development dependencies installed."
