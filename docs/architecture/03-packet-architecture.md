# 03 — Packet Architecture

Status: Draft v0.1.2. Field layouts are logical until fixed by the NLS specification; byte-level formats are **[reference required]**. Markers: **[Specified]**, **[Decision pending]**, **[Not implemented]**.

## 1. Packet families

| Plane | Family | Role |
|---|---|---|
| Control | **NLS-OSPF** | routing: neighbor discovery, adjacency, advertisements, key-state exchange |
| Control | **NLS-VIP** | VIP exchange used to establish secured communication with a destination router |
| Data | **NLS-Secured-Packet** | protected user traffic: the inner packet is encrypted and authenticated |
| Data | **Normal Packet** | ordinary traffic forwarded without NLS protection (where policy allows) |
| Data | **Others** | any other traffic: ICMP, ARP/ND, management, IPsec, TLS and unclassified traffic, handled per its own module |

Mapping to the earlier module layout: `packet/common` is the shared header, `packet/vip` is NLS-VIP, `packet/payload/normal` is Normal Packet, `packet/payload/encrypted` is NLS-Secured-Packet.

## 2. Common header (logical)

Fields expected in every NLS packet: version, packet type (family and subtype), length, and integrity/authentication coverage indicator. Exact fields and sizes: **[reference required]**. Type values are allocated only by the specification.

## 3. NLS-VIP packets

Purpose: carry the VIP and the exchange that results in a secured association with a destination router. Logical contents: VIP, sender identity reference, key-establishment material, authentication data. Exact message sequence and formats: **[reference required]**. NLS-VIP packets are control-plane packets and are handled by the control plane, not forwarded by the data plane.

## 4. NLS-Secured-Packet

Carries a whole protected inner packet. Logical contents: header with session reference and sequence/replay information, ciphertext, authentication tag. Processing requires a valid session published by the control plane (`05`). Cipher, tag size and header layout: security specification **[reference required]**.

## 5. Normal Packet and Others

Normal packets are forwarded by the installed FIB. Whether NLS-required prefixes may ever send a Normal Packet is governed by policy: traffic that policy marks as protected is never sent as a Normal Packet. Others are passed to their owning module and are outside NLS processing.

## 6. VIP

| Property | Definition |
|---|---|
| What it is | A **temporary identity** used to initiate secured communication |
| Generation | Produced with a **SHA hash algorithm**. Hash variant and exact inputs are defined only by the NLS specification **[reference required]**; this document does not define a formula |
| Lifetime | Valid only while secured communication is being set up. **After secured communication is established the VIP expires.** An unused VIP also expires after a bounded time **[Decision pending: duration]** |
| Not the same as | original IP address, router identifier, certificate fingerprint, public key, session identifier |
| Security note | A hash value is an identifier, not proof of identity. Authentication of the peer comes from certificates and signatures validated against Router-CA trust (`07`), never from the VIP alone |

VIP lifecycle states (logical): generated, in use (exchange in progress), consumed (secured communication established), expired, rejected.

## 7. Classification rules (intended)

1. Match NLS-OSPF and NLS-VIP by protocol identification: deliver to the control plane.
2. Match NLS-Secured-Packet: session lookup and verification (`05`).
3. Everything else is a Normal Packet or Others by policy and module matching.

Identification mechanism (protocol number, port, header marker): **[reference required]**.

## 8. Malformed and unexpected packets

Drop, count, rate-limited log. No state change. Unknown NLS types are dropped, never forwarded as Normal Packets.
