-- NLS/OSPF Link-State Advertisement
CREATE TABLE IF NOT EXISTS lsa (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ls_type SMALLINT UNSIGNED NOT NULL,
    link_state_id VARCHAR(64) NOT NULL,
    advertising_router VARCHAR(64) NOT NULL,
    ls_sequence_number BIGINT UNSIGNED NOT NULL,
    ls_checksum INT UNSIGNED NOT NULL,
    length INT UNSIGNED NOT NULL,
    age_at_install INT UNSIGNED NOT NULL DEFAULT 0,
    link_count INT UNSIGNED NULL,
    payload LONGBLOB NULL,
    source_neighbor_id BIGINT UNSIGNED NULL,
    installed_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    refreshed_at DATETIME(6) NULL,
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_lsa_identity (ls_type, link_state_id, advertising_router),
    KEY idx_lsa_sequence (advertising_router, ls_sequence_number),
    CONSTRAINT fk_lsa_source_neighbor FOREIGN KEY (source_neighbor_id) REFERENCES neighbor(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
