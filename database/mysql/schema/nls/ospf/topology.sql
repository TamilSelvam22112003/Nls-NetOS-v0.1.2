-- NLS / OSPF TOPOLOGY TABLE
-- Stores topology relationships derived from the accepted LSDB.

CREATE TABLE IF NOT EXISTS nls_topology (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_id INT UNSIGNED NOT NULL,
    neighbor_id INT UNSIGNED NOT NULL,
    advertising_router INT UNSIGNED NOT NULL,
    link_state_id INT UNSIGNED NOT NULL,
    interface_id INT UNSIGNED NULL,
    area_id INT UNSIGNED NOT NULL DEFAULT 0,
    cost INT UNSIGNED NOT NULL,
    link_state VARCHAR(32) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_topology_link (router_id, neighbor_id, link_state_id),
    KEY idx_nls_topology_advertising_router (advertising_router),
    KEY idx_nls_topology_neighbor (neighbor_id),
    KEY idx_nls_topology_area (area_id),
    KEY idx_nls_topology_updated_at (updated_at)
);
