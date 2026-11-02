"""NLS packet architecture.

Packet families are separated by plane and ownership:
- ``common``: shared logical NLS packet structures
- ``ospf``: control-plane NLS-OSPF packets
- ``vip``: control-plane NLS-VIP packets
- ``payload.normal``: data-plane ordinary inner/user packets
- ``payload.encrypted``: data-plane NLS-Secured-Packet protected payloads

Byte-level wire layouts remain specification-controlled and must not be
invented here while the authoritative NLS wire specification is pending.
"""
