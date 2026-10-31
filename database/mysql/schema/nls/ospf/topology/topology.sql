-- NLS/OSPF Network Topology
CREATE TABLE IF NOT EXISTS topology (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    local_router_id VARCHAR(64) NOT NULL,
    neighbor_router_id VARCHAR(64) NOT NULL,
    local_interface_name VARCHAR(64) NULL,
    local_port_number INT UNSIGNED NULL,
    remote_interface_name VARCHAR(64) NULL,
    remote_port_number INT UNSIGNED NULL,
    link_type VARCHAR(32) NULL,
    metric INT UNSIGNED NOT NULL DEFAULT 1,
    state VARCHAR(32) NOT NULL DEFAULT 'UP',
    source_lsa_id BIGINT UNSIGNED NULL,
    last_calculated_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_topology_link (local_router_id, neighbor_router_id, local_interface_name),
    KEY idx_topology_neighbor (neighbor_router_id),
    CONSTRAINT fk_topology_source_lsa FOREIGN KEY (source_lsa_id) REFERENCES lsa(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
