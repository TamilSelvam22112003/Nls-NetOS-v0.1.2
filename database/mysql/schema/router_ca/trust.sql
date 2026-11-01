CREATE TABLE IF NOT EXISTS router_ca_trust (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_ca_id BIGINT UNSIGNED NOT NULL,
    trust_anchor_fingerprint CHAR(64) NOT NULL,
    trust_level ENUM('root','intermediate','provider','peer','conditional') NOT NULL,
    validation_policy VARCHAR(255) NULL,
    valid_from DATETIME NULL,
    valid_to DATETIME NULL,
    status ENUM('trusted','pending','rejected','revoked','expired') NOT NULL DEFAULT 'pending',
    last_validated_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_trust_anchor (router_ca_id, trust_anchor_fingerprint),
    CONSTRAINT fk_router_ca_trust_ca FOREIGN KEY (router_ca_id) REFERENCES router_ca(id)
) ENGINE=InnoDB;
