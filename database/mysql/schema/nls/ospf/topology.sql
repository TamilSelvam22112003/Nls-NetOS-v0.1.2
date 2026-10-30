-- OSPFv2 SPF TOPOLOGY
-- Relational representation of the OSPF shortest-path graph derived from the LSDB.

CREATE TABLE IF NOT EXISTS nls_topology (
    area_id INT UNSIGNED NOT NULL,

    vertex_id INT UNSIGNED NOT NULL,
    vertex_type TINYINT UNSIGNED NOT NULL,

    link_id INT UNSIGNED NOT NULL,
    link_type TINYINT UNSIGNED NOT NULL,
    link_data INT UNSIGNED NOT NULL,
    metric INT UNSIGNED NOT NULL,

    PRIMARY KEY (area_id, vertex_id, vertex_type, link_id, link_type),
    KEY idx_nls_topology_vertex (area_id, vertex_id, vertex_type),
    KEY idx_nls_topology_link (area_id, link_id, link_type),
    KEY idx_nls_topology_metric (metric)
);
