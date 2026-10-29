-- NLS LSDB TRUST TABLE
--
-- Trust and cryptographic state associated with an NLS neighbor.
-- sync_key must contain protected/encrypted material or a secure key-store
-- reference. Do not store plaintext private asymmetric keys in MySQL.

CREATE TABLE IF NOT EXISTS nls_lsdb_trust (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- Neighbor identity and reachability
    neighbor_id INT UNSIGNED NOT NULL,
    interface_id VARCHAR(32) NOT NULL,
    neighbor_ip VARCHAR(64) NOT NULL,

    -- Key identity / rollover
    key_id INT UNSIGNED NOT NULL,
    sync_key VARBINARY(512) NULL,
    async_key VARBINARY(512) NULL,
    key_status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',

    -- Protocol adjacency state
    link_state VARCHAR(20) NOT NULL DEFAULT 'DOWN',

    -- Security / traffic counters
    rx_packet_count BIGINT UNSIGNED NOT NULL DEFAULT 0,
    tx_packet_count BIGINT UNSIGNED NOT NULL DEFAULT 0,
    auth_failure_count BIGINT UNSIGNED NOT NULL DEFAULT 0,

    -- Liveness
    last_seen_timestamp TIMESTAMP NULL DEFAULT NULL,

    -- Record lifecycle
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_lsdb_trust_neighbor_interface (neighbor_id, interface_id),
    KEY idx_nls_lsdb_trust_neighbor (neighbor_id),
    KEY idx_nls_lsdb_trust_key_id (key_id),
    KEY idx_nls_lsdb_trust_key_status (key_status),
    KEY idx_nls_lsdb_trust_link_state (link_state),
    KEY idx_nls_lsdb_trust_last_seen (last_seen_timestamp)
);
