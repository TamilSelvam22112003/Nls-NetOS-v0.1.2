CREATE TABLE IF NOT EXISTS router_ca_authorization (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_ca_id BIGINT UNSIGNED NOT NULL,
    subject_fingerprint CHAR(64) NOT NULL,
    authorization_type ENUM('provider','router_admin','system','bootstrap') NOT NULL,
    permission_set VARCHAR(2048) NOT NULL,
    valid_from DATETIME NULL,
    valid_to DATETIME NULL,
    status ENUM('active','expired','revoked','disabled') NOT NULL DEFAULT 'active',
    last_used_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_authorization (router_ca_id, subject_fingerprint, authorization_type),
    CONSTRAINT fk_router_ca_auth_ca FOREIGN KEY (router_ca_id) REFERENCES router_ca(id)
) ENGINE=InnoDB;
