-- NLS/OSPF Trust Verification Request
CREATE TABLE IF NOT EXISTS verification_request (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    session_id BIGINT UNSIGNED NOT NULL,
    request_uuid CHAR(36) NOT NULL,
    request_type VARCHAR(32) NOT NULL DEFAULT 'IDENTITY_VERIFY',
    local_router_id VARCHAR(64) NOT NULL,
    neighbor_router_id VARCHAR(64) NULL,
    neighbor_ip VARCHAR(64) NULL,
    local_interface_name VARCHAR(64) NULL,
    local_port_number INT UNSIGNED NULL,
    nonce VARBINARY(64) NOT NULL,
    requested_fields JSON NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    sent_at DATETIME(6) NULL,
    received_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_verification_request_uuid (request_uuid),
    KEY idx_verification_request_session (session_id),
    CONSTRAINT fk_verification_request_session FOREIGN KEY (session_id) REFERENCES verification_session(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
