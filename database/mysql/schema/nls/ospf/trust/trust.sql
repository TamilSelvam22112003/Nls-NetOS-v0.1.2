-- NLS/OSPF Trusted Neighbor Security Authority
--
-- Security-critical authorization state for OSPF/NLS.
-- This table is the gate between successful identity verification
-- and operational neighbor/adjacency/LSA/LSDB/topology/routing state.
-- Actual private keys and secret symmetric-key material MUST NOT be stored here.

CREATE TABLE IF NOT EXISTS trust (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- Router identity
    local_router_id VARCHAR(64) NOT NULL,
    neighbor_router_id VARCHAR(64) NOT NULL,
    neighbor_ip VARCHAR(64) NOT NULL,
    router_version VARCHAR(64) NULL,

    -- Local/remote interface and physical/logical port mapping
    local_interface_name VARCHAR(64) NULL,
    local_interface_index INT UNSIGNED NULL,
    local_port_number INT UNSIGNED NULL,
    remote_interface_name VARCHAR(64) NULL,
    remote_interface_index INT UNSIGNED NULL,
    remote_port_number INT UNSIGNED NULL,
    link_type VARCHAR(32) NULL,
    link_state VARCHAR(32) NOT NULL DEFAULT 'UP',

    -- Router-CA identity and certificate state
    router_ca_identity_id VARCHAR(128) NULL,
    certificate_id VARCHAR(128) NULL,
    certificate_serial VARCHAR(128) NULL,
    certificate_fingerprint CHAR(64) NULL,
    certificate_status VARCHAR(32) NOT NULL DEFAULT 'UNKNOWN',
    certificate_valid_from DATETIME(6) NULL,
    certificate_valid_until DATETIME(6) NULL,
    certificate_revoked_at DATETIME(6) NULL,

    -- Public-key identity/reference
    public_key_id VARCHAR(128) NULL,
    public_key_algorithm VARCHAR(32) NULL,
    public_key_size SMALLINT UNSIGNED NULL,
    public_key_version VARCHAR(64) NULL,
    public_key_fingerprint CHAR(64) NULL,
    public_key_status VARCHAR(32) NOT NULL DEFAULT 'UNKNOWN',

    -- Synchronous-key metadata only
    synchronous_key_id VARCHAR(128) NULL,
    synchronous_key_version VARCHAR(64) NULL,
    synchronous_key_epoch BIGINT UNSIGNED NULL,
    synchronous_key_fingerprint CHAR(64) NULL,
    synchronous_key_state VARCHAR(32) NOT NULL DEFAULT 'UNINITIALIZED',
    synchronous_key_valid_from DATETIME(6) NULL,
    synchronous_key_valid_until DATETIME(6) NULL,
    synchronous_key_secure_storage_ref VARCHAR(256) NULL,

    -- Asynchronous-key metadata only
    asynchronous_key_id VARCHAR(128) NULL,
    asynchronous_key_version VARCHAR(64) NULL,
    asynchronous_key_epoch BIGINT UNSIGNED NULL,
    asynchronous_key_fingerprint CHAR(64) NULL,
    asynchronous_key_state VARCHAR(32) NOT NULL DEFAULT 'UNINITIALIZED',
    asynchronous_key_valid_from DATETIME(6) NULL,
    asynchronous_key_valid_until DATETIME(6) NULL,
    asynchronous_key_secure_storage_ref VARCHAR(256) NULL,

    -- Verification evidence reference
    verification_session_id BIGINT UNSIGNED NULL,
    identity_verified BOOLEAN NOT NULL DEFAULT FALSE,
    certificate_verified BOOLEAN NOT NULL DEFAULT FALSE,
    public_key_verified BOOLEAN NOT NULL DEFAULT FALSE,
    cryptographic_proof_verified BOOLEAN NOT NULL DEFAULT FALSE,
    path_verified BOOLEAN NOT NULL DEFAULT FALSE,

    -- Trust authorization
    trust_state VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    trust_level VARCHAR(32) NOT NULL DEFAULT 'NONE',
    trust_reason VARCHAR(255) NULL,

    -- OSPF/NLS authorization gate
    neighbor_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    adjacency_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    lsa_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    lsdb_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    topology_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    routing_allowed BOOLEAN NOT NULL DEFAULT FALSE,

    -- Security lifecycle
    trusted_at DATETIME(6) NULL,
    valid_until DATETIME(6) NULL,
    revoked_at DATETIME(6) NULL,
    last_verified_at DATETIME(6) NULL,
    last_key_rotation_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),

    -- Optimistic concurrency / state version
    record_version BIGINT UNSIGNED NOT NULL DEFAULT 1,

    PRIMARY KEY (id),
    UNIQUE KEY uq_trust_neighbor (local_router_id, neighbor_router_id, neighbor_ip),
    KEY idx_trust_interface (local_interface_name, local_port_number),
    KEY idx_trust_state (trust_state, trust_level, link_state),
    KEY idx_trust_certificate (certificate_fingerprint),
    KEY idx_trust_public_key (public_key_fingerprint),
    KEY idx_trust_sync_key (synchronous_key_id, synchronous_key_epoch),
    KEY idx_trust_async_key (asynchronous_key_id, asynchronous_key_epoch),
    KEY idx_trust_verification (verification_session_id),
    KEY idx_trust_ospf_permissions (
        neighbor_allowed,
        adjacency_allowed,
        lsa_allowed,
        lsdb_allowed,
        topology_allowed,
        routing_allowed
    ),

    CONSTRAINT chk_trust_public_key_size
        CHECK (public_key_size IS NULL OR public_key_size IN (2048, 3072, 4096)),
    CONSTRAINT chk_trust_certificate_dates
        CHECK (
            certificate_valid_until IS NULL OR
            certificate_valid_from IS NULL OR
            certificate_valid_until >= certificate_valid_from
        ),
    CONSTRAINT chk_trust_permissions
        CHECK (
            trust_state = 'TRUSTED'
            OR (
                neighbor_allowed = FALSE AND
                adjacency_allowed = FALSE AND
                lsa_allowed = FALSE AND
                lsdb_allowed = FALSE AND
                topology_allowed = FALSE AND
                routing_allowed = FALSE
            )
        )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- SECURITY REQUIREMENT:
-- Never store private keys, plaintext synchronous keys, plaintext asynchronous
-- keys, passwords, or other secret cryptographic material in this table.
-- Store only key identifiers, versions, epochs, fingerprints, lifecycle state,
-- and references into the router's protected cryptographic storage.
