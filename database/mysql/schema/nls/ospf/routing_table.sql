-- OSPFv2 ROUTING TABLE
-- Relational representation of the OSPF routing table described in RFC 2328.

CREATE TABLE IF NOT EXISTS nls_routing_table (
    destination_type TINYINT UNSIGNED NOT NULL,
    destination_id INT UNSIGNED NOT NULL,
    address_mask INT UNSIGNED NOT NULL,
    area_id INT UNSIGNED NOT NULL,

    path_type TINYINT UNSIGNED NOT NULL,
    cost INT UNSIGNED NOT NULL,
    type_2_cost INT UNSIGNED NULL,

    link_state_origin_type TINYINT UNSIGNED NOT NULL,
    link_state_origin_id INT UNSIGNED NOT NULL,
    link_state_origin_router INT UNSIGNED NOT NULL,

    next_hop INT UNSIGNED NOT NULL,
    outgoing_interface INT UNSIGNED NOT NULL,

    PRIMARY KEY (
        area_id,
        destination_type,
        destination_id,
        address_mask,
        path_type,
        next_hop,
        outgoing_interface
    ),
    KEY idx_nls_route_destination (destination_id, address_mask),
    KEY idx_nls_route_path_type (path_type),
    KEY idx_nls_route_cost (cost),
    KEY idx_nls_route_origin (
        link_state_origin_type,
        link_state_origin_id,
        link_state_origin_router
    ),
    KEY idx_nls_route_next_hop (next_hop)
);
