-- NLS/OSPF Neighbor State
CREATE TABLE IF NOT EXISTS neighbor (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    local_router_id VARCHAR(64) NOT NULL,
    neighbor_router_id VARCHAR(64) NOT NULL,
    neighbor_ip VARCHAR(64) NOT NULL,
    local_interface_name VARCHAR(64) NOT NULL,
    local_port_number INT UNSIGNED NULL,
    remote_interface_name VARCHAR(64) NULL,
    remote_port_number INT UNSIGNED NULL,
    neighbor_state VARCHAR(32) NOT NULL DEFAULT 'DOWN',
    neighbor_priority INT UNSIGNED NULL,
    router_dead_interval INT UNSIGNED NULL,
    last_hello_at DATETIME(6) NULL,
    last_state_change_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_neighbor_link (local_router_id, neighbor_router_id, neighbor_ip, local_interface_name),
    KEY idx_neighbor_state (neighbor_state),
    KEY idx_neighbor_port (local_interface_name, local_port_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
