-- OSPFv2 LINK STATE ADVERTISEMENT
-- Relational representation of the OSPF LSA header and body from RFC 2328.

CREATE TABLE IF NOT EXISTS nls_lsa (
    ls_age INT UNSIGNED NOT NULL DEFAULT 0,
    options TINYINT UNSIGNED NOT NULL DEFAULT 0,
    ls_type TINYINT UNSIGNED NOT NULL,
    link_state_id INT UNSIGNED NOT NULL,
    advertising_router INT UNSIGNED NOT NULL,
    ls_sequence_number INT NOT NULL,
    ls_checksum SMALLINT UNSIGNED NOT NULL,
    length SMALLINT UNSIGNED NOT NULL,

    -- LSA body. The interpretation is determined by LS Type.
    body LONGBLOB NULL,

    PRIMARY KEY (ls_type, link_state_id, advertising_router),
    KEY idx_nls_lsa_advertising_router (advertising_router),
    KEY idx_nls_lsa_sequence (ls_sequence_number),
    KEY idx_nls_lsa_checksum (ls_checksum)
);
