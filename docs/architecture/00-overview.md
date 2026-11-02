# 00 — Architecture Overview

Status: Draft v0.1.2. Markers: **[Specified]** defined by the NLS specification or stated by the project owner, **[Decision pending]** unresolved (to be recorded as an ADR), **[Not implemented]** design intent with no implementation evidence.

## 1. Terminology

| Term | Meaning |
|---|---|
| **NLS** | The network-layer protocol that secures router-to-router communication by encrypting and decrypting the packet. The NLS specification is the single authoritative source for protocol definitions. |
| **NLS-NetOS** | The router operating system that implements NLS and hosts the planes below. |
| **NLS-OSPF** | The NLS routing subsystem (modified OSPF) with extra tables for neighbor cryptographic material. |
| **VIP** | A **temporary identity** generated with a SHA hash algorithm, used to set up secured communication with a destination router. It expires once secured communication is established. See `03` and `04`. |
| **NLS-VIP** | The control-plane packet family that carries the VIP exchange. |
| **NLS-Secured-Packet** | The data-plane packet carrying protected (encrypted) traffic. |
| **Router-CA** | The certificate authority each router connects to while booting. |
| **Symmetric / asymmetric keys** | Referred to in project documents as synchronous and asynchronous keys. This document set uses symmetric and asymmetric. |

NLS-NetOS is the system; NLS is the protocol. Neither name stands for the other.

## 2. Planes

| Plane | Contains | Packet families |
|---|---|---|
| Management | CLI, configuration, telemetry, audit logging | none (API/CLI) |
| Control | NLS-OSPF, NLS-VIP/session management, RIB, FIB manager, neighbor and interface management, policy, Router-CA client | NLS-OSPF, NLS-VIP |
| Data | classification, NLS packet protection, forwarding from installed FIB, transmission | NLS-Secured-Packet, Normal Packet, Others |
| Cross-cutting | cryptographic subsystem, database, observability | none |

## 3. Component responsibilities

| Component | Owns | Does not own |
|---|---|---|
| Platform | hardware init, CPU/memory/PCI, drivers, hardware crypto access | protocol state |
| Control plane | routing protocol operations, adjacency and topology state, route calculation, VIP and session establishment, policy | packet encryption/decryption, forwarding |
| RIB | selected routes | topology database |
| FIB manager | publishing forwarding entries to the data plane | route calculation |
| Data plane | packet classification, protection and verification, FIB lookup, transmission | SPF, LSDB, VIP negotiation |
| Cryptographic subsystem | key-pair generation, secure key storage, algorithm providers, hashing | trust or routing decisions |
| Router-CA | certificates, trust anchors, status/revocation, peer information | router private keys, session keys |
| Database | persistent configuration and protocol metadata | secret key material, transient state |
| Management plane | CLI, configuration, telemetry | protocol state machines |

## 4. Boundaries

- Control plane to data plane: RIB/FIB publication and session installation interfaces only (`08`).
- Control plane to Router-CA: authenticated request/response (`07`, `08`).
- All components to crypto: through the crypto service interface; secrets stay in the key store (`07`).
- Process model **[Decision pending]**: a component is called a daemon only when an ADR or the implementation says so. The Router-CA server is a separately deployable service; the router holds only the Router-CA client.

## 5. State classes

| Class | Examples | Survives restart |
|---|---|---|
| Persistent configuration | interfaces, routing, NLS policy, CA endpoints | yes |
| Persistent protocol metadata | identity, certificate references, trust, key identifiers and validity | yes, re-validated on load |
| Secret material | private keys, symmetric secrets | only per key-management design |
| Transient runtime state | adjacencies, VIPs, sessions, replay windows, counters, installed FIB | no, re-established |

## 6. Document map

`01` boot · `02` NLS-OSPF · `03` packet architecture (including VIP) · `04` control plane · `05` data plane · `06` database · `07` security · `08` module interfaces.

## 7. Open decisions

Process/daemon split; hash variant and exact inputs for VIP (specification); Router-CA offline policy and cache age; CA topology; readiness thresholds; stale-FIB period; ACL/firewall/NAT ordering relative to NLS; secret storage; first fast-path technology. Per-feature implementation status defaults to [Not implemented] until evidence exists.
