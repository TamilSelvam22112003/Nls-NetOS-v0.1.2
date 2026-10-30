-- NLS / OSPF ROUTING TABLE
-- Stores routes selected by route calculation from the topology.

CREATE TABLE IF NOT EXISTS nls_routing_table (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_id INT UNSIGNED NOT NULL,
    destination VARBINARY(16) NOT NULL,
    prefix_length TINYINT UNSIGNED NOT NULL,
    address_family TINYINT UNSIGNED NOT NULL,
    next_hop VARBINARY(16) NULL,
    outgoing_interface_id INT UNSIGNED NULL,
    metric BIGINT UNSIGNED NOT NULL,
    route_type VARCHAR(32) NOT NULL,
    area_id INT UNSIGNED NULL,
    source_lsa_id BIGINT UNSIGNED NULL,
    protocol VARCHAR(16) NOT NULL DEFAULT 'NLS',
    installed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_route (router_id, destination, prefix_length, address_family),
    KEY idx_nls_route_next_hop (next_hop),
    KEY idx_nls_route_interface (outgoing_interface_id),
    KEY idx_nls_route_metric (metric),
    KEY idx_nls_route_source_lsa (source_lsa_id),
    KEY idx_nls_route_updated_at (updated_at)
);
