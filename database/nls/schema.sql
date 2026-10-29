-- NLS ROUTING DATABASE SCHEMA
--
-- Scope:
--   Persistent protocol state needed by the NLS routing/control-plane work.
--
-- This directory is intentionally separate from database/mysql/.
-- Trust/authentication policy is NOT defined here. The Trust Table will be
-- integrated later when the NLS trust design is finalized.
--
-- Storage model:
--   nls_neighbors      -> directly connected neighbor/adjacency state
--   nls_lsdb           -> accepted link-state advertisements (LSDB)
--   nls_topology       -> derived topology representation used by SPF
--   nls_routing_table  -> selected/installed routing state
--
-- Packet rule:
--   Hello -> neighbor state
--   DBD   -> database synchronization state (comparison only)
--   LSR   -> outstanding LSA request state
--   LSU   -> accepted LSA -> LSDB -> topology -> SPF -> routing table
--   LSAck -> acknowledgment/retransmission state
--
-- OSPF packet metadata itself is not treated as routing-table data. The
-- packet-processing layer should decode and validate it before persisting
-- protocol state.

PRAGMA foreign_keys = ON;

-- ============================================================
-- 1. Neighbor Table
-- ============================================================
-- Maintains the latest directly connected NLS neighbor state.
-- Trust/authentication ownership remains outside this schema for now.

CREATE TABLE IF NOT EXISTS nls_neighbors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    neighbor_id INTEGER NOT NULL,
    interface_id INTEGER,
    neighbor_ip TEXT NOT NULL,

    -- Authentication/trust identifiers carried by the NLS neighbor state.
    -- Validation and policy are owned by the future Trust Table/component.
    key_id INTEGER,
    key_version INTEGER,

    link_state TEXT NOT NULL DEFAULT 'down',
    neighbor_state TEXT NOT NULL DEFAULT 'down',

    hello_interval INTEGER,
    dead_interval INTEGER,
    router_priority INTEGER,
    designated_router TEXT,
    backup_designated_router TEXT,

    dd_sequence_number INTEGER,
    outstanding_lsa_requests INTEGER NOT NULL DEFAULT 0,
    outstanding_retransmissions INTEGER NOT NULL DEFAULT 0,

    last_hello_at TEXT,
    last_seen_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (neighbor_id, interface_id)
);

CREATE INDEX IF NOT EXISTS idx_nls_neighbors_neighbor_id
    ON nls_neighbors (neighbor_id);

CREATE INDEX IF NOT EXISTS idx_nls_neighbors_state
    ON nls_neighbors (neighbor_state);

-- ============================================================
-- 2. Link-State Database (LSDB)
-- ============================================================
-- Stores the current accepted LSA for each LSA identity.
--
-- LS Age is protocol state. Do NOT increment it every second in SQL.
-- Runtime code derives current age from installed_at/age state.
-- The payload contains the type-specific LSA body.

CREATE TABLE IF NOT EXISTS nls_lsdb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- LSA identity
    ls_type INTEGER NOT NULL,
    link_state_id INTEGER NOT NULL,
    advertising_router INTEGER NOT NULL,

    -- LSA header / freshness / integrity
    ls_age INTEGER NOT NULL DEFAULT 0,
    ls_sequence_number INTEGER NOT NULL,
    ls_checksum INTEGER NOT NULL,
    ls_length INTEGER NOT NULL,

    -- LSA body
    link_count INTEGER,
    payload BLOB NOT NULL,

    -- Installation context
    source_neighbor_id INTEGER,
    installed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (ls_type, link_state_id, advertising_router),

    FOREIGN KEY (source_neighbor_id)
        REFERENCES nls_neighbors (neighbor_id)
        ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_nls_lsdb_type
    ON nls_lsdb (ls_type);

CREATE INDEX IF NOT EXISTS idx_nls_lsdb_link_state_id
    ON nls_lsdb (link_state_id);

CREATE INDEX IF NOT EXISTS idx_nls_lsdb_advertising_router
    ON nls_lsdb (advertising_router);

CREATE INDEX IF NOT EXISTS idx_nls_lsdb_sequence
    ON nls_lsdb (ls_sequence_number);

CREATE INDEX IF NOT EXISTS idx_nls_lsdb_source_neighbor
    ON nls_lsdb (source_neighbor_id);

-- ============================================================
-- 3. Topology Table / Derived Topology Cache
-- ============================================================
-- This is derived from the LSDB. It is NOT a second source of truth.
-- It can be rebuilt from nls_lsdb after restart or after topology changes.

CREATE TABLE IF NOT EXISTS nls_topology (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    advertising_router INTEGER NOT NULL,
    link_id INTEGER NOT NULL,
    link_type INTEGER NOT NULL,
    link_data TEXT,
    neighbor_router_id INTEGER,
    network_prefix TEXT,
    metric INTEGER NOT NULL DEFAULT 0,

    source_lsdb_id INTEGER NOT NULL,
    topology_version INTEGER NOT NULL DEFAULT 1,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (
        advertising_router,
        link_id,
        link_type,
        source_lsdb_id
    ),

    FOREIGN KEY (source_lsdb_id)
        REFERENCES nls_lsdb (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_nls_topology_router
    ON nls_topology (advertising_router);

CREATE INDEX IF NOT EXISTS idx_nls_topology_neighbor
    ON nls_topology (neighbor_router_id);

CREATE INDEX IF NOT EXISTS idx_nls_topology_network
    ON nls_topology (network_prefix);

-- ============================================================
-- 4. Routing Table
-- ============================================================
-- Stores routes selected by SPF/route selection. It is derived state,
-- not a copy of the LSDB.

CREATE TABLE IF NOT EXISTS nls_routing_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    destination_prefix TEXT NOT NULL,
    prefix_length INTEGER NOT NULL,
    next_hop TEXT,
    outgoing_interface INTEGER,

    metric INTEGER NOT NULL,
    route_type TEXT NOT NULL,
    area_id INTEGER,

    source_router_id INTEGER,
    topology_version INTEGER,
    installed INTEGER NOT NULL DEFAULT 0,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (
        destination_prefix,
        prefix_length,
        next_hop,
        outgoing_interface,
        route_type
    )
);

CREATE INDEX IF NOT EXISTS idx_nls_routes_destination
    ON nls_routing_table (destination_prefix, prefix_length);

CREATE INDEX IF NOT EXISTS idx_nls_routes_next_hop
    ON nls_routing_table (next_hop);

CREATE INDEX IF NOT EXISTS idx_nls_routes_metric
    ON nls_routing_table (metric);

CREATE INDEX IF NOT EXISTS idx_nls_routes_installed
    ON nls_routing_table (installed);
