-- NLS/OSPF Trust Verification Session
CREATE TABLE IF NOT EXISTS verification_session (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    session_uuid CHAR(36) NOT NULL,
    local_router_id VARCHAR(64) NOT NULL,
    neighbor_router_id VARCHAR(64) NULL,
    neighbor_ip VARCHAR(64) NULL,
    local_interface_name VARCHAR(64) NULL,
    local_port_number INT UNSIGNED NULL,
    verification_type VARCHAR(32) NOT NULL DEFAULT 'IDENTITY',
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    started_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    completed_at DATETIME(6) NULL,
    expires_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_verification_session_uuid (session_uuid),
    KEY idx_verification_session_neighbor (neighbor_router_id, neighbor_ip),
    KEY idx_verification_session_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
