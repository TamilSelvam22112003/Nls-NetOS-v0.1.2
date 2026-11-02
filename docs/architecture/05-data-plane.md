# 05 — Data Plane

Status: Draft v0.1.2. The pipeline order is the intended design and must be matched to the final NLS encapsulation design. Markers: **[Specified]**, **[Decision pending]**, **[Not implemented]**.

## 1. Boundary

The data plane forwards using installed FIB entries and installed session state. It does not run SPF, does not hold the LSDB, and does not negotiate VIPs or keys. Those are control-plane functions delivered through the interfaces in `08`.

## 2. Packet classes handled

| Class | Handling |
|---|---|
| NLS-Secured-Packet | verify, decrypt, then forward; or protect then send |
| Normal Packet | forward by FIB if policy allows unprotected traffic |
| Others | handed to the owning module (ICMP, ARP/ND, management, IPsec, TLS, etc.) |
| NLS-OSPF and NLS-VIP | delivered to the control plane, not forwarded |

## 3. Pipeline (intended)

Ingress: receive, initial validation (length, header sanity), classify, security processing (for NLS-Secured-Packet: session lookup, authentication, replay check, decrypt), FIB lookup, next-hop selection, egress checks, NLS protection if the egress path requires it, transmit.

Position of ACL, firewall and NAT relative to NLS steps: **[Decision pending]**.

## 4. Security functions are separate

| Function | Purpose | Note |
|---|---|---|
| Encryption | confidentiality | does not alone authenticate or stop replay |
| Authentication and integrity | origin and integrity | mechanism in security specification |
| Replay check | reject duplicates and old packets | per-session sequence state |
| Routing lookup | choose next hop | on authenticated, decrypted data only |
| Forwarding | transmit | last |

## 5. Session and gate

Per destination, a protected send requires an installed valid session. Session state held here is limited to key handles, session identifier, epoch, expiry and replay window. VIPs are not used for data forwarding; they are expired before data flows. Keys are referenced through the key store, not copied into tables.

## 6. Interfaces from the control plane

- FIB: add, replace, delete, full synchronization with completion marker.
- Session: install, replace (rekey), remove (expiry or revocation), atomic per destination.

Install errors return to the control plane, which retries. The data plane is not ready until initial sync completes. Stale entries survive a bounded period after a control-plane restart **[Decision pending]**.

## 7. Failure handling

| Condition | Behaviour |
|---|---|
| No route | drop, count, ICMP per policy |
| Next hop unavailable | drop or alternate, count |
| Missing or invalid session | drop protected traffic, signal control plane |
| Malformed packet | drop, count, rate-limited log |
| Authentication failure | drop, count, alert threshold |
| Expired key | treat as invalid session, drop, request rekey |
| Replay | drop, count |

## 8. Other modules and fast path

ACL, QoS, NAT, firewall, IPsec and TLS are handled by their modules; none is claimed implemented or enabled without evidence, and interaction with NLS is **[Decision pending]**. Kernel path, userspace engine, XDP, eBPF, DPDK and hardware offload are possible implementation choices, **[Not implemented]**, to be chosen by ADR.
