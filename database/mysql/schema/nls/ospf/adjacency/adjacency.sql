-- NLS/OSPF Adjacency State
CREATE TABLE IF NOT EXISTS adjacency (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    neighbor_id BIGINT UNSIGNED NOT NULL,
    local_router_id VARCHAR(64) NOT NULL,
    neighbor_router_id VARCHAR(64) NOT NULL,
    state VARCHAR(32) NOT NULL DEFAULT 'DOWN',
    master_router_id VARCHAR(64) NULL,
    dd_sequence_number BIGINT UNSIGNED NULL,
    last_dbd_at DATETIME(6) NULL,
    last_lsr_at DATETIME(6) NULL,
    last_lsu_at DATETIME(6) NULL,
    last_lsack_at DATETIME(6) NULL,
    state_changed_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_adjacency_neighbor (neighbor_id),
    KEY idx_adjacency_state (state),
    CONSTRAINT fk_adjacency_neighbor FOREIGN KEY (neighbor_id) REFERENCES neighbor(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
