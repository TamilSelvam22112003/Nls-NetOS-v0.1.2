-- OSPFv2 NEIGHBOR DATA STRUCTURE
-- Relational representation of the OSPF Neighbor Data Structure from RFC 2328.

CREATE TABLE IF NOT EXISTS nls_neighbor (
    router_id INT UNSIGNED NOT NULL,
    interface_id INT UNSIGNED NOT NULL,
    area_id INT UNSIGNED NOT NULL,

    neighbor_id INT UNSIGNED NOT NULL,
    neighbor_ip INT UNSIGNED NULL,
    neighbor_priority TINYINT UNSIGNED NOT NULL DEFAULT 0,
    neighbor_options TINYINT UNSIGNED NOT NULL DEFAULT 0,

    state VARCHAR(16) NOT NULL,
    designated_router INT UNSIGNED NOT NULL DEFAULT 0,
    backup_designated_router INT UNSIGNED NOT NULL DEFAULT 0,

    dd_sequence_number INT UNSIGNED NULL,
    last_dd_initialize BOOLEAN NOT NULL DEFAULT FALSE,
    last_dd_more BOOLEAN NOT NULL DEFAULT FALSE,
    last_dd_master BOOLEAN NOT NULL DEFAULT FALSE,
    last_dd_options TINYINT UNSIGNED NULL,
    last_dd_sequence_number INT UNSIGNED NULL,

    -- OSPF neighbor LSA lists.
    -- Each value contains the LSA identity tuples maintained by the
    -- protocol: (LS type, Link State ID, Advertising Router).
    link_state_retransmission_list JSON NULL,
    database_summary_list JSON NULL,
    link_state_request_list JSON NULL,

    PRIMARY KEY (router_id, interface_id, neighbor_id),
    KEY idx_nls_neighbor_area (area_id),
    KEY idx_nls_neighbor_state (state),
    KEY idx_nls_neighbor_ip (neighbor_ip)
);
