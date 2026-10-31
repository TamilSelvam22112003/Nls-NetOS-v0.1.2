-- NLS/OSPF Calculated Routing Table
CREATE TABLE IF NOT EXISTS routing_table (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_id VARCHAR(64) NOT NULL,
    destination VARCHAR(128) NOT NULL,
    prefix_length TINYINT UNSIGNED NOT NULL,
    address_family TINYINT UNSIGNED NOT NULL DEFAULT 4,
    next_hop VARCHAR(64) NULL,
    outgoing_interface VARCHAR(64) NULL,
    outgoing_port_number INT UNSIGNED NULL,
    metric BIGINT UNSIGNED NOT NULL DEFAULT 0,
    route_type VARCHAR(32) NOT NULL DEFAULT 'OSPF',
    source_lsa_id BIGINT UNSIGNED NULL,
    path_cost BIGINT UNSIGNED NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    installed_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_routing_destination (router_id, destination, prefix_length, address_family),
    KEY idx_routing_next_hop (next_hop),
    KEY idx_routing_interface (outgoing_interface, outgoing_port_number),
    CONSTRAINT fk_routing_source_lsa FOREIGN KEY (source_lsa_id) REFERENCES lsa(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
