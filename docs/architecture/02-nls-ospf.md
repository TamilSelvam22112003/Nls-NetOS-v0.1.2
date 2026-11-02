# 02 — NLS-OSPF

Status: Draft v0.1.2. Describes architecture and ownership. Wire formats, state machines, timers and cryptographic mechanisms are defined only by the NLS specification and are referenced here. Markers: **[Specified]**, **[Decision pending]**, **[Not implemented]**.

## 1. Relationship to OSPF

NLS-OSPF is the NLS routing subsystem. It is an **independent protocol that reuses OSPF concepts** (neighbors, adjacency, link-state advertisements, LSDB, SPF, routing table) and adds tables for neighbor cryptographic material. It is **not** designed to interoperate with standard OSPF.

- Packet formats, state machines and timers are not assumed identical to OSPF.
- No interoperability with standard OSPF is claimed or planned.
- The unmodified baseline `ospf` module stays separate from `nls_ospf`.

## 2. NLS-OSPF packets

NLS-OSPF packets are a control-plane packet family (`03`). They are distinct from NLS-VIP packets. Types, formats and fields: **[reference required]**.

## 3. Additional tables beyond standard OSPF

| Table | Purpose |
|---|---|
| Neighbor key table | neighbor public-key or certificate reference, key identifier, validity, status |
| Trust table | trust decision per neighbor identity, derived from Router-CA data |
| Verification table | outcome and time of neighbor identity verification |
| Key-state table in the LSDB | key state advertised or learned per router |

Tables hold metadata and references, not secret key material (`06`, `07`).

## 4. State ownership

| State | Owner | Consumers |
|---|---|---|
| Neighbor and adjacency state | NLS-OSPF | CLI, telemetry |
| LSDB and topology | NLS-OSPF | SPF |
| Neighbor key metadata | NLS-OSPF, validated against Router-CA trust | NLS-VIP and session manager |
| Route results | NLS-OSPF to RIB | RIB |
| RIB | RIB | FIB manager |
| FIB | FIB manager publishes, data plane holds installed copy | data plane |

The data plane does not run SPF or hold the LSDB.

## 5. Acceptance of routing information

An advertisement is accepted only when, in order: it is well-formed; the sender is an authenticated peer in a state that allows the message; the integrity and authentication check passes; freshness, ordering, duplicate and retransmission rules pass. Algorithms and replay protection are defined in the security specification (`07`).

## 6. Authentication and adjacency

Messages allowed before a secure association exists, and messages that require authenticated peer state, are listed from the specification **[reference required]**. A full adjacency requires authenticated peer state. Neighbor keys are stored only after validation against Router-CA trust.

## 7. Failure and recovery

| Event | Behaviour |
|---|---|
| Malformed message | discard, count, rate-limited log |
| Authentication failure | discard, no adjacency change, alert per policy |
| Stale advertisement | ignore per sequence and age rules |
| Adjacency loss | withdraw topology, recompute, update RIB and FIB |
| Peer revoked | tear down adjacency, purge neighbor metadata and advertisements |
| Restart | rebuild adjacencies and LSDB, FIB reconciliation per `01` |

Timers are **[Decision pending / reference required]**. No message type is claimed implemented without evidence.
