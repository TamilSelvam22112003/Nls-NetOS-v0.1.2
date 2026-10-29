-- NLS Link State Database
--
-- Stores the current protocol-level state of each Link State Advertisement.
-- The protocol process derives live LS Age from installation/refresh state;
-- it should not rewrite this table once per second.

CREATE TABLE IF NOT EXISTS nls_lsdb (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- LSA header / identity
    ls_age INT UNSIGNED NOT NULL DEFAULT 0,
    ls_type SMALLINT UNSIGNED NOT NULL,
    link_state_id INT UNSIGNED NOT NULL,
    advertising_router INT UNSIGNED NOT NULL,

    -- LSA version / integrity
    ls_sequence_number INT UNSIGNED NOT NULL,
    ls_checksum SMALLINT UNSIGNED NOT NULL,
    length SMALLINT UNSIGNED NOT NULL,

    -- Context-dependent LSA payload metadata
    link_count INT UNSIGNED NULL,
    payload LONGBLOB NULL,

    -- Neighbor from which this LSA was learned, when applicable
    source_neighbor_id INT UNSIGNED NULL,

    -- Persistence / refresh metadata
    installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_lsdb_lsa (
        ls_type,
        link_state_id,
        advertising_router
    ),
    KEY idx_nls_lsdb_advertising_router (advertising_router),
    KEY idx_nls_lsdb_type (ls_type),
    KEY idx_nls_lsdb_sequence (ls_sequence_number),
    KEY idx_nls_lsdb_source_neighbor (source_neighbor_id),
    KEY idx_nls_lsdb_updated_at (updated_at)
);

-- LSDB TRUST TABLE
--
-- Per-neighbor trust/key state used when protecting NLS communication.
-- Plaintext private asymmetric keys or long-lived secret key material must
-- not be stored here. sync_key should contain protected/encrypted key
-- material or a secure key-store reference according to deployment policy.

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
