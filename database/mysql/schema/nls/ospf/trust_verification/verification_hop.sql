-- NLS/OSPF Verification Hop Evidence
CREATE TABLE IF NOT EXISTS verification_hop (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    session_id BIGINT UNSIGNED NOT NULL,
    hop_number INT UNSIGNED NOT NULL,
    router_id VARCHAR(64) NOT NULL,
    router_ip VARCHAR(64) NULL,
    previous_router_id VARCHAR(64) NULL,
    next_router_id VARCHAR(64) NULL,
    ingress_interface_name VARCHAR(64) NULL,
    ingress_port_number INT UNSIGNED NULL,
    egress_interface_name VARCHAR(64) NULL,
    egress_port_number INT UNSIGNED NULL,
    hop_nonce VARBINARY(64) NULL,
    hop_signature MEDIUMBLOB NULL,
    public_key_fingerprint CHAR(64) NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'RECEIVED',
    reason TEXT NULL,
    observed_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_verification_hop_session_number (session_id, hop_number),
    KEY idx_verification_hop_router (router_id, router_ip),
    CONSTRAINT fk_verification_hop_session FOREIGN KEY (session_id) REFERENCES verification_session(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
