-- NLS/OSPF Verification Result
CREATE TABLE IF NOT EXISTS verification_result (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    session_id BIGINT UNSIGNED NOT NULL,
    comparison_id BIGINT UNSIGNED NULL,
    status VARCHAR(32) NOT NULL,
    trust_eligible BOOLEAN NOT NULL DEFAULT FALSE,
    identity_verified BOOLEAN NOT NULL DEFAULT FALSE,
    certificate_verified BOOLEAN NOT NULL DEFAULT FALSE,
    key_verified BOOLEAN NOT NULL DEFAULT FALSE,
    signature_verified BOOLEAN NOT NULL DEFAULT FALSE,
    path_verified BOOLEAN NOT NULL DEFAULT FALSE,
    rejection_code VARCHAR(64) NULL,
    rejection_reason TEXT NULL,
    verified_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    KEY idx_verification_result_session (session_id),
    CONSTRAINT fk_verification_result_session FOREIGN KEY (session_id) REFERENCES verification_session(id),
    CONSTRAINT fk_verification_result_comparison FOREIGN KEY (comparison_id) REFERENCES identity_comparison(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
