# 04 — Control Plane

Status: Draft v0.1.2. Markers: **[Specified]**, **[Decision pending]**, **[Not implemented]**.

## 1. Responsibilities

| Component | Responsibility |
|---|---|
| NLS-OSPF | neighbor discovery, adjacency, LSDB, SPF, neighbor key tables (`02`) |
| NLS-VIP manager | generate VIPs, run the NLS-VIP exchange, expire VIPs |
| Session manager | establish, rekey, expire and revoke secured sessions; publish them to the data plane |
| Router-CA client | enrollment, certificate, trust, status and policy synchronization |
| Policy | which prefixes and peers require NLS |
| RIB | selected routes |
| FIB manager | publish forwarding entries and session state to the data plane |
| Interface and neighbor management | interface state, neighbor tracking |
| CLI and management | configuration and inspection (management plane) |

Which of these are separate processes is **[Decision pending]**.

## 2. Secured communication setup (intended flow)

1. Policy says traffic to a destination router requires NLS and no valid session exists.
2. The NLS-VIP manager generates a **VIP** (temporary identity, SHA-based, inputs per specification).
3. NLS-VIP packets are exchanged with the destination router.
4. The peer is validated against Router-CA trust: certificate chain, status, authorization. Fresh peer information is requested from Router-CA when cached data is missing or too old.
5. Keys are established by the specified key-agreement exchange; the asymmetric keys authenticate it and symmetric session keys protect traffic.
6. The session manager records session metadata and passes key handles to the data plane through the session installation interface (`08`).
7. Once secured communication is established, **the VIP expires** and is removed. Data traffic then uses NLS-Secured-Packets.

Exact messages and ordering: **[reference required]**. Failure at any step: no session installed, VIP expires, policy decides drop, queue or retry.

## 3. Gate rule

The data plane may protect or accept protected traffic for a destination only when the control plane has published a valid, unexpired session for it, backed by a valid, trusted identity and key metadata (asymmetric and symmetric stored separately, `06`). If missing: trigger establishment, queue or drop per policy. Traffic that policy marks as protected is never sent unprotected.

## 4. Ownership of records

| Record | Created and changed by | Expired or deleted by |
|---|---|---|
| Identity and trust metadata | Router-CA client | Router-CA client on expiry or revocation |
| Neighbor key metadata | NLS-OSPF after validation | NLS-OSPF or revocation event |
| VIP records | NLS-VIP manager | NLS-VIP manager on completion, timeout or failure |
| Session records | session manager | session manager on expiry, rekey, revocation |

Other components read only.

## 5. Routing outputs

NLS-OSPF results go to the RIB; the FIB manager converts the RIB into forwarding entries and publishes them (add, replace, delete, full sync). The data plane never reads the LSDB.

## 6. Events affecting the control plane

| Event | Effect |
|---|---|
| Certificate expiry | renewal; no new sessions if expired |
| Peer revoked | adjacency down, neighbor metadata purged, sessions and VIPs invalidated, FIB updated |
| Router-CA unreachable | per `07` offline policy |
| Key rotation | new key epoch, rekey sessions |
| Restart | rebuild adjacencies, discard VIPs and sessions, re-establish, reconcile FIB (`01`) |
