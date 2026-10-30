-- NLS / OSPF NEIGHBOR TABLE
-- Stores protocol neighbors and their current neighbor state.

CREATE TABLE IF NOT EXISTS nls_neighbor (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_id INT UNSIGNED NOT NULL,
    neighbor_id INT UNSIGNED NOT NULL,
    neighbor_ip VARBINARY(16) NOT NULL,
    interface_id INT UNSIGNED NULL,
    area_id INT UNSIGNED NOT NULL DEFAULT 0,
    state VARCHAR(32) NOT NULL,
    priority SMALLINT UNSIGNED NOT NULL DEFAULT 1,
    dr_router_id INT UNSIGNED NULL,
    bdr_router_id INT UNSIGNED NULL,
    last_hello_at TIMESTAMP NULL DEFAULT NULL,
    last_state_change_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_nls_neighbor (router_id, neighbor_id, interface_id),
    KEY idx_nls_neighbor_neighbor_id (neighbor_id),
    KEY idx_nls_neighbor_state (state),
    KEY idx_nls_neighbor_interface (interface_id),
    KEY idx_nls_neighbor_updated_at (updated_at)
);
