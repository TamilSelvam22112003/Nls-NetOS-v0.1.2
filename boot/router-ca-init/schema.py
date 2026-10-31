"""Persistent Router-CA data model.

The schema is intentionally portable SQL. Actual secret/private-key material
must not be stored in these metadata tables; store a secure-storage reference.
"""

SCHEMA_SQL = r'''
CREATE TABLE IF NOT EXISTS router_ca_profile (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    alias VARCHAR(128) NOT NULL,
    ca_identifier VARCHAR(255) NOT NULL,
    group_name VARCHAR(128) NULL,
    source_type ENUM('manufacturer','isp','cloud','enterprise','local','other') NOT NULL DEFAULT 'other',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    explicitly_untrusted BOOLEAN NOT NULL DEFAULT FALSE,
    enrollment_protocol ENUM('none','est','scep','acme') NOT NULL DEFAULT 'none',
    enrollment_url VARCHAR(2048) NULL,
    enrollment_auth_ref VARCHAR(255) NULL,
    bootstrap_token_ref VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_profile_alias (alias),
    UNIQUE KEY uq_router_ca_profile_identifier (ca_identifier)
);

CREATE TABLE IF NOT EXISTS router_ca_certificate (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    profile_id BIGINT UNSIGNED NOT NULL,
    certificate_format ENUM('der','pem') NOT NULL,
    certificate_blob LONGBLOB NOT NULL,
    public_key_blob BLOB NULL,
    public_key_algorithm VARCHAR(64) NULL,
    public_key_bits INT UNSIGNED NULL,
    ski VARBINARY(64) NULL,
    fingerprint_sha256 BINARY(32) NOT NULL,
    fingerprint_sha512 BINARY(64) NULL,
    subject_dn TEXT NOT NULL,
    issuer_dn TEXT NOT NULL,
    serial_number VARCHAR(512) NOT NULL,
    not_before DATETIME(6) NOT NULL,
    not_after DATETIME(6) NOT NULL,
    signature_algorithm VARCHAR(128) NULL,
    is_trust_anchor BOOLEAN NOT NULL DEFAULT TRUE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_cert_fingerprint (fingerprint_sha256),
    KEY ix_router_ca_cert_profile (profile_id),
    KEY ix_router_ca_cert_expiry (not_after),
    CONSTRAINT fk_router_ca_cert_profile FOREIGN KEY (profile_id) REFERENCES router_ca_profile(id)
);

CREATE TABLE IF NOT EXISTS router_ca_revocation (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    profile_id BIGINT UNSIGNED NOT NULL,
    crl_distribution_point VARCHAR(2048) NULL,
    crl_blob LONGBLOB NULL,
    crl_number VARCHAR(255) NULL,
    this_update DATETIME(6) NULL,
    next_update DATETIME(6) NULL,
    fetched_at DATETIME(6) NULL,
    ocsp_responder_url VARCHAR(2048) NULL,
    ocsp_signing_certificate_id BIGINT UNSIGNED NULL,
    status ENUM('unknown','good','revoked','expired','unreachable') NOT NULL DEFAULT 'unknown',
    PRIMARY KEY (id),
    KEY ix_router_ca_revocation_profile (profile_id),
    CONSTRAINT fk_router_ca_revocation_profile FOREIGN KEY (profile_id) REFERENCES router_ca_profile(id),
    CONSTRAINT fk_router_ca_revocation_ocsp_cert FOREIGN KEY (ocsp_signing_certificate_id) REFERENCES router_ca_certificate(id)
);

CREATE TABLE IF NOT EXISTS router_ca_policy (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    profile_id BIGINT UNSIGNED NOT NULL,
    allowed_name_constraints TEXT NULL,
    excluded_name_constraints TEXT NULL,
    allowed_eku TEXT NULL,
    path_length_constraint INT NULL,
    allow_server_auth BOOLEAN NOT NULL DEFAULT FALSE,
    allow_client_auth BOOLEAN NOT NULL DEFAULT FALSE,
    allow_nls_auth BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_policy_profile (profile_id),
    CONSTRAINT fk_router_ca_policy_profile FOREIGN KEY (profile_id) REFERENCES router_ca_profile(id)
);

CREATE TABLE IF NOT EXISTS router_ca_assignment (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    profile_id BIGINT UNSIGNED NOT NULL,
    subsystem ENUM('ipsec','https','8021x','restconf','netconf','nls','system') NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_assignment (profile_id, subsystem),
    CONSTRAINT fk_router_ca_assignment_profile FOREIGN KEY (profile_id) REFERENCES router_ca_profile(id)
);

CREATE TABLE IF NOT EXISTS router_ca_sync_state (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    profile_id BIGINT UNSIGNED NOT NULL,
    endpoint VARCHAR(2048) NOT NULL,
    last_success_at DATETIME(6) NULL,
    last_attempt_at DATETIME(6) NULL,
    next_refresh_at DATETIME(6) NULL,
    last_error TEXT NULL,
    remote_version VARCHAR(128) NULL,
    state ENUM('pending','connecting','synchronized','stale','failed') NOT NULL DEFAULT 'pending',
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_sync_profile (profile_id),
    CONSTRAINT fk_router_ca_sync_profile FOREIGN KEY (profile_id) REFERENCES router_ca_profile(id)
);

CREATE TABLE IF NOT EXISTS router_ca_key_reference (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    profile_id BIGINT UNSIGNED NOT NULL,
    key_identifier VARCHAR(255) NOT NULL,
    key_algorithm VARCHAR(64) NOT NULL,
    key_bits INT UNSIGNED NULL,
    storage_provider VARCHAR(128) NOT NULL,
    secure_storage_ref VARCHAR(512) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rotated_at TIMESTAMP NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_router_ca_key_reference (key_identifier),
    CONSTRAINT fk_router_ca_key_profile FOREIGN KEY (profile_id) REFERENCES router_ca_profile(id)
);
'''
