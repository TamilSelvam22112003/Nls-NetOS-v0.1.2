# NLS-NetOS-v0.1.2 — NLS Database

This directory is the database boundary for the NLS routing/control-plane state used by `Nls-NetOS-v0.1.2`.

The repository already contains the NLS runtime/control-plane implementation under `src/router_os/control_plane/routing/nls/`. The database schema here is kept aligned with that design without changing unrelated repository areas.

## Tables

| Table | Role | Source / update path |
|---|---|---|
| `nls_neighbors` | Neighbor and adjacency state | Hello + adjacency/DBD/LSR/LSU/LSAck processing |
| `nls_lsdb` | Current accepted LSAs | Valid/newer LSU contents and locally originated LSAs |
| `nls_topology` | Derived topology graph/cache | Rebuilt/updated from the LSDB |
| `nls_routing_table` | Selected routes | SPF + route selection + installation |

## OSPF packet flow

```text
Hello
  -> Neighbor state

DBD
  -> Compare LSA headers with local LSDB

LSR
  -> Request missing/newer LSA

LSU
  -> Validate LSA
  -> nls_lsdb
  -> nls_topology
  -> SPF / route selection
  -> nls_routing_table

LSAck
  -> Acknowledgment / retransmission state
```

DBD, LSR, and LSAck are protocol-exchange/control information. They do not directly become routing entries.

## Metadata vs payload

The packet-processing layer is responsible for decoding the network packet before persistence.

- IP metadata: source IP, destination IP, protocol, TTL, etc.
- OSPF metadata: version, packet type, packet length, Router ID, Area ID, checksum/authentication fields as applicable.
- LSA metadata: LS Age, LS Type, Link State ID, Advertising Router, sequence number, checksum, length.
- LSA payload: type-specific topology information such as links, relationships, networks, and metrics.

`nls_lsdb.payload` stores the type-specific LSA body. The LSA header fields are stored separately so freshness and identity can be checked without decoding the body every time.

## Design boundary

The LSDB is the source of truth for accepted link-state advertisements. The topology and routing tables are derived state.

The **Trust Table is intentionally not created here yet**. Authentication/trust policy will be added when the Trust design is finalized. The neighbor schema only retains identifiers such as `key_id`/`key_version` needed to associate protocol state with that future trust layer.

No OSPF packet-capture/history table is added at this stage; packet transport metadata belongs to the protocol-processing layer unless persistent packet history is explicitly required later.
