-- OSPFv2 LINK STATE DATABASE
-- The OSPF LSDB is the collection of LSAs for an area.
-- This relational table stores the current LSA instances that make up that database.

CREATE TABLE IF NOT EXISTS nls_lsdb (
    area_id INT UNSIGNED NOT NULL,

    ls_age INT UNSIGNED NOT NULL DEFAULT 0,
    options TINYINT UNSIGNED NOT NULL DEFAULT 0,
    ls_type TINYINT UNSIGNED NOT NULL,
    link_state_id INT UNSIGNED NOT NULL,
    advertising_router INT UNSIGNED NOT NULL,
    ls_sequence_number INT NOT NULL,
    ls_checksum SMALLINT UNSIGNED NOT NULL,
    length SMALLINT UNSIGNED NOT NULL,

    -- LSA body; interpretation is determined by LS Type.
    body LONGBLOB NULL,

    PRIMARY KEY (area_id, ls_type, link_state_id, advertising_router),
    KEY idx_nls_lsdb_advertising_router (advertising_router),
    KEY idx_nls_lsdb_type (ls_type),
    KEY idx_nls_lsdb_sequence (ls_sequence_number),
    KEY idx_nls_lsdb_checksum (ls_checksum)
);
