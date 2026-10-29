-- NLS Link State Database
--
-- Stores the protocol-level identity, versioning, integrity metadata,
-- and opaque payload for each installed Link State Advertisement (LSA).

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

    -- Optional context-dependent payload metadata
    link_count INT UNSIGNED NULL,
    payload LONGBLOB NULL,

    -- Synchronization source
    source_neighbor_id INT UNSIGNED NULL,

    -- Persistence metadata
    installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),

    -- One current LSA per type, Link State ID, and Advertising Router.
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

-- LS Age is protocol state. The NLS process should calculate elapsed age
-- from its installation/refresh state rather than repeatedly rewriting the
-- database once per second. A received LSA must not exceed the protocol's
-- configured maximum age (3600 seconds) when accepted as current state.
