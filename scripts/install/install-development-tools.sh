#!/usr/bin/env bash
set -Eeuo pipefail
for tool in git gcc make cmake python3 ip vtysh tcpdump openssl sqlite3; do
  if command -v "$tool" >/dev/null 2>&1; then echo "OK   $tool"; else echo "MISS $tool"; fi
done
if command -v docker >/dev/null 2>&1; then docker --version; else echo "Docker is optional and not installed."; fi
