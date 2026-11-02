# 08 — Module Interfaces

Status: Draft v0.1.2. Interface names and operations are logical contracts; concrete transport (library call, IPC, gRPC, shared memory) is **[Decision pending]**. Markers: **[Specified]**, **[Decision pending]**, **[Not implemented]**.

## 1. Interface table

| # | Provider | Consumer | Operations (logical) | Notes |
|---|---|---|---|---|
| I1 | Boot orchestrator | all boot stages | start stage, report status, enforce dependencies and failure policy | owns stage ordering (`01`) |
| I2 | Crypto subsystem | boot, control plane, data plane | generate key pair (asymmetric), generate symmetric key material, store, use by handle, hash, sign, verify, destroy | secrets never returned as plain values to callers that do not need them |
| I3 | Key store | crypto subsystem | store, load, rotate, delete by key identifier | secure hardware where present |
| I4 | Database access | all control-plane modules | read, write by record owner, schema versioned | not on packet hot path (`06`) |
| I5 | Router-CA server | Router-CA client | enroll, renew, peer-info, status, trust update, authorization policy | authenticated channel (`07`) |
| I6 | Router-CA client | NLS-OSPF, NLS-VIP manager, session manager | get certificate, get peer info, check status, subscribe to revocation events | single local path to the CA |
| I7 | NLS-OSPF | NLS-VIP manager | neighbor key metadata, adjacency state | read access to neighbor key tables |
| I8 | NLS-OSPF | RIB | route add, replace, delete | route results |
| I9 | NLS-VIP manager | crypto subsystem | generate VIP hash, nonce, key-agreement operations | VIP inputs per specification |
| I10 | NLS-VIP manager | session manager | exchange completed, VIP consumed, exchange failed | triggers VIP expiry |
| I11 | Session manager | data plane | install, replace (rekey), remove session; atomic per destination | carries key handles, not secrets |
| I12 | RIB | FIB manager | selected routes | |
| I13 | FIB manager | data plane | add, replace, delete, full sync with completion marker | install errors returned |
| I14 | Data plane | control plane | request session establishment, report authentication failure, expiry, replay events | signaling channel |
| I15 | Policy | NLS-VIP manager, data plane | which prefixes or peers require NLS | |
| I16 | Management plane (CLI) | all | configuration set, state read, audit | no direct state mutation outside owners |
| I17 | Telemetry and audit | all | metrics, events, audit records | no secrets |

## 2. Rules

- Data plane to control plane access only through I11, I13, I14.
- The data plane never reads the LSDB, neighbor tables or VIP tables.
- A record is written only by its owner (`04` §4).
- Secrets cross module boundaries only as key handles.
- VIPs stay inside the control plane except as NLS-VIP packet content.

## 3. Packet delivery

| Packet | Delivered to |
|---|---|
| NLS-OSPF | NLS-OSPF |
| NLS-VIP | NLS-VIP manager |
| NLS-Secured-Packet | data-plane NLS engine |
| Normal Packet | data-plane forwarding |
| Others | owning module |

## 4. Cross-document consistency

| Contract | Source | Status |
|---|---|---|
| NLS-NetOS versus NLS naming | `00` | OK |
| NLS-OSPF is independent, reuses OSPF concepts, no standard OSPF interoperability | `02` | OK |
| Control plane owns routing state and SPF | `02`, `04` | OK |
| Data plane consumes FIB and sessions through interfaces | `05`, `08` | OK |
| VIP: temporary SHA-based identity, expires after secured communication | `03`, `04`, `06`, `07` | OK, exact inputs need specification reference |
| Identity, certificate, trust, VIP, session are distinct | `03`, `06`, `07` | OK |
| Private-key and secret ownership | `07` | Unresolved (router symmetric key role, secrets in tables) |
| Boot order matches implementation | `01` | Unresolved, map to systemd units |
| Router-CA offline policy | `01`, `07` | Unresolved |
| Unimplemented features not claimed | all | OK |

## 5. Open decisions

Process split; interface transport; VIP hash variant, inputs and timeout; router symmetric key role; Router-CA offline policy; CA topology; stale-FIB period; ACL/firewall/NAT ordering; first fast-path technology.
