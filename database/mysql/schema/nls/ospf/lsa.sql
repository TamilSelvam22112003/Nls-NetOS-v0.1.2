-- NLS / OSPF LINK STATE ADVERTISEMENT
-- Stores individual LSA records received, originated, or retained for protocol use.

CREATE TABLE IF NOT EXISTS nls_lsa (
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
    UNIQUE KEY uq_nls_lsa (ls_type, link_state_id, advertising_router, ls_sequence_number),
    KEY idx_nls_lsa_advertising_router (advertising_router),
    KEY idx_nls_lsa_source_neighbor (source_neighbor_id),
    KEY idx_nls_lsa_sequence (ls_sequence_number),
    KEY idx_nls_lsa_updated_at (updated_at),

    CONSTRAINT chk_nls_lsa_age CHECK (ls_age <= 3600),
    CONSTRAINT chk_nls_lsa_length CHECK (length > 0)
);
