# NLS dependency matrix

| Dependency | Package/tool | NLS use | Required |
|---|---|---|---|
| FRRouting | frr, frr-pythontools | Zebra, OSPFv2/OSPFv3, VTYSH | Routing integration |
| Python | python3, venv, pip | NLS services | Yes |
| cryptography | Python package | AES-GCM, X25519, HKDF, signatures | Yes |
| Scapy | Python package | Packet crafting and tests | Development |
| pyroute2 | Python package | Netlink and route operations | Yes |
| PyYAML | Python package | YAML configuration | Yes |
| SQLite | sqlite3, libsqlite3-dev | Local state | Yes |
| OpenSSL | openssl, libssl-dev | Certificate tooling | Yes |
| iproute2 | iproute2 | Interface and route inspection | Yes |
| nftables | nftables | Firewall integration | Network labs |
| tcpdump | tcpdump | Packet capture | Debugging |
| GCC/CMake/Ninja | build packages | Native builds | Yes |
| pytest/Ruff/mypy | Python dev extras | Tests, lint, type checks | Development |
| Docker | Docker Engine | Reproducible labs | Optional |
| Mininet | Mininet | Multi-router simulation | Optional |
| Wireshark | Wireshark GUI | Packet inspection | Optional |
| PostgreSQL | PostgreSQL server | Future multi-node DB option | Optional |

FRR versions vary by Ubuntu release. Pin and validate a specific FRR version before production image builds.
