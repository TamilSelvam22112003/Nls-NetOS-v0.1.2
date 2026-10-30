-- NLS / OSPF OBSERVATION VIEW
-- One read-only view for observing the main NLS state together.

CREATE OR REPLACE VIEW nls_ospf_overview AS
SELECT
    n.id AS neighbor_record_id,
    n.router_id,
    n.neighbor_id,
    n.state AS neighbor_state,
    t.id AS topology_record_id,
    t.link_state_id,
    t.cost AS topology_cost,
    r.id AS route_record_id,
    r.destination,
    r.prefix_length,
    r.next_hop,
    r.metric,
    r.route_type,
    l.id AS lsdb_record_id,
    l.ls_type,
    l.advertising_router,
    l.ls_sequence_number,
    l.ls_checksum,
    a.id AS lsa_record_id,
    a.ls_age AS lsa_age,
    tr.key_id,
    tr.key_version,
    tr.key_type,
    tr.key_state,
    tr.trust_state,
    v.vip_address,
    v.state AS vip_state
FROM nls_neighbor n
LEFT JOIN nls_topology t
    ON t.router_id = n.router_id
   AND t.neighbor_id = n.neighbor_id
LEFT JOIN nls_routing_table r
    ON r.router_id = n.router_id
LEFT JOIN nls_lsdb l
    ON l.advertising_router = t.advertising_router
   AND l.link_state_id = t.link_state_id
LEFT JOIN nls_lsa a
    ON a.ls_type = l.ls_type
   AND a.link_state_id = l.link_state_id
   AND a.advertising_router = l.advertising_router
LEFT JOIN nls_trust tr
    ON tr.router_id = n.router_id
   AND tr.neighbor_id = n.neighbor_id
LEFT JOIN nls_vip v
    ON v.router_id = n.router_id;
