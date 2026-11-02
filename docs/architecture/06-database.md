# 06 — Database

Status: Draft v0.1.2. The table lists are a **logical data model** until reconciled with `database/mysql/schema/**`. Existing columns are not changed by this document. Markers: **[Specified]**, **[Decision pending]**, **[Not implemented]**.

## 1. Role

The database holds persistent configuration and protocol metadata. It is not on the packet hot path. Runtime decisions use in-memory tables loaded from, and optionally written back to, the database **[Decision pending: memory as source of truth versus database]**.

## 2. What is not stored

Private keys and symmetric secrets are held only by the key store (secure hardware or encrypted store), referenced by identifier. Database tables store identifiers, references, algorithm information, validity and status, not unrestricted secret key material. If a design needs secrets in tables, an ADR must define protection first.

## 3. Logical tables

### 3.1 Own identity and keys
| Table | Contents |
|---|---|
| router_identity | router identifier, certificate reference, validity, status |
| own_key_metadata | key identifier, kind (asymmetric or symmetric), algorithm, creation time, validity, key-store reference |

### 3.2 Router-CA
| Table | Contents |
|---|---|
| ca_provider | CA endpoints and provider list |
| ca_trust | trust anchors and their status |
| ca_certificate | issued certificate references |
| ca_key_state | key state and revocation information with freshness time |
| ca_authorization | permitted operations per identity |
| ca_sync | last synchronization time and result |

### 3.3 NLS-OSPF additions
| Table | Contents |
|---|---|
| neighbor_key | neighbor identity, certificate or public-key reference, key identifier, validity, status |
| neighbor_trust | trust decision and its source |
| neighbor_verification | verification outcome and time |
| lsdb_key_state | per-router key state in the LSDB |

### 3.4 Destination-router key metadata (two separate tables)
| Table | Contents |
|---|---|
| peer_asymmetric_key | peer identity, public key or certificate reference, key identifier, algorithm, validity, status |
| peer_symmetric_key | peer identity, session key identifier, algorithm, lifetime, epoch, rekey state, key-store reference |

### 3.5 VIP and sessions
| Table | Contents |
|---|---|
| vip | VIP value, associated peer identity, state (generated, in use, consumed, expired, rejected), creation and expiry time |
| session | session identifier, peer, key epoch, state, expiry; replay counters are runtime only |

## 4. VIP records are short-lived

A VIP record exists from generation until secured communication is established or the VIP times out; it then moves to expired and is purged by the NLS-VIP manager. VIP records need not survive a restart **[Decision pending]**; the default is to discard them at start.

## 5. Ownership

Each record class has one writer (`04` §4); all other components read only.

## 6. Persistent versus runtime

| Persistent | Runtime only |
|---|---|
| configuration, identity, trust, key metadata, certificate references | VIPs in progress, session state, replay windows, counters, timers, installed FIB |

## 7. Layout and migrations

Schemas live under `database/mysql/schema/nls/*`, migrations under `migrations/`, seeds under `seeds/`. Two duplicated Router-CA schema directories in the current tree must be merged **[Decision pending]**.

## 8. Reconciliation task

Compare the logical tables above with the actual schema and list differences (field, logical, actual, resolution) before accepting this document.
