-- NLS VIP TABLE
-- Stores the NLS Virtual IP identity associated with a router.

CREATE TABLE IF NOT EXISTS nls_vip (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_id INT UNSIGNED NOT NULL,
    vip_address VARBINARY(16) NOT NULL,
    address_family TINYINT UNSIGNED NOT NULL,
    state VARCHAR(32) NOT NULL,
    valid_from TIMESTAMP NULL DEFAULT NULL,
    valid_until TIMESTAMP NULL DEFAULT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_vip (router_id, vip_address, address_family),
    KEY idx_nls_vip_state (state),
    KEY idx_nls_vip_updated_at (updated_at)
);
