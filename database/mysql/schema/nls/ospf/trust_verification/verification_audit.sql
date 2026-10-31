-- NLS/OSPF Verification Audit Trail
CREATE TABLE IF NOT EXISTS verification_audit (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    session_id BIGINT UNSIGNED NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    actor_router_id VARCHAR(64) NULL,
    event_status VARCHAR(32) NULL,
    event_reason TEXT NULL,
    event_data JSON NULL,
    event_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    KEY idx_verification_audit_session (session_id),
    KEY idx_verification_audit_event (event_type, event_at),
    CONSTRAINT fk_verification_audit_session FOREIGN KEY (session_id) REFERENCES verification_session(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
