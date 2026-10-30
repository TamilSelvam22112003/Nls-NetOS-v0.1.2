-- NLS TRUST TABLE
-- Stores trust and cryptographic key state associated with NLS neighbors.

CREATE TABLE IF NOT EXISTS nls_trust (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_id INT UNSIGNED NOT NULL,
    neighbor_id INT UNSIGNED NOT NULL,
    advertising_router INT UNSIGNED NOT NULL,
    source_router_id INT UNSIGNED NOT NULL,
    key_id INT UNSIGNED NOT NULL,
    key_version INT UNSIGNED NOT NULL,
    key_type VARCHAR(32) NOT NULL,
    key_tag VARCHAR(16) NOT NULL,
    synchronous_key_ref VARCHAR(255) NULL,
    synchronous_key_algorithm VARCHAR(64) NULL,
    asynchronous_public_key BLOB NULL,
    key_state VARCHAR(32) NOT NULL,
    valid_from TIMESTAMP NULL DEFAULT NULL,
    valid_until TIMESTAMP NULL DEFAULT NULL,
    revoked_at TIMESTAMP NULL DEFAULT NULL,
    trust_state VARCHAR(32) NOT NULL,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_trust_key (router_id, key_id, key_version, key_tag),
    KEY idx_nls_trust_neighbor (neighbor_id),
    KEY idx_nls_trust_advertising_router (advertising_router),
    KEY idx_nls_trust_source_router (source_router_id),
    KEY idx_nls_trust_key_state (key_state),
    KEY idx_nls_trust_trust_state (trust_state),
    KEY idx_nls_trust_valid_until (valid_until),
    KEY idx_nls_trust_revoked_at (revoked_at)
);
