-- NLS / OSPF LINK STATE DATABASE
-- Stores the current accepted Link State Advertisement state.

CREATE TABLE IF NOT EXISTS nls_lsdb (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ls_type SMALLINT UNSIGNED NOT NULL,
    link_state_id INT UNSIGNED NOT NULL,
    advertising_router INT UNSIGNED NOT NULL,
    ls_age INT UNSIGNED NOT NULL DEFAULT 0,
    ls_sequence_number INT NOT NULL,
    ls_checksum SMALLINT UNSIGNED NOT NULL,
    length SMALLINT UNSIGNED NOT NULL,
    link_count INT UNSIGNED NULL,
    payload LONGBLOB NULL,
    source_neighbor_id INT UNSIGNED NULL,
    installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_lsdb_lsa (ls_type, link_state_id, advertising_router),
    KEY idx_nls_lsdb_link_state_id (link_state_id),
    KEY idx_nls_lsdb_advertising_router (advertising_router),
    KEY idx_nls_lsdb_type (ls_type),
    KEY idx_nls_lsdb_sequence (ls_sequence_number),
    KEY idx_nls_lsdb_source_neighbor (source_neighbor_id),
    KEY idx_nls_lsdb_updated_at (updated_at),

    CONSTRAINT chk_nls_lsdb_age CHECK (ls_age <= 3600),
    CONSTRAINT chk_nls_lsdb_length CHECK (length > 0)
);
