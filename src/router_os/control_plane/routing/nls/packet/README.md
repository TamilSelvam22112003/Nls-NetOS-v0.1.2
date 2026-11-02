# NLS Packet Architecture

This package separates NLS packet ownership by control-plane/data-plane role.

```text
packet/
├── common/
│   └── Shared NLS packet structures
├── ospf/
│   └── CONTROL PLANE — NLS-OSPF packets
├── vip/
│   └── CONTROL PLANE — NLS-VIP packets
└── payload/
    ├── normal/
    │   └── DATA PLANE — ordinary inner/user packet representation
    └── encrypted/
        └── DATA PLANE — NLS-Secured-Packet protected inner packet
```

## Ownership

- `common/` contains structures shared by NLS packet families.
- `ospf/` contains the control-plane NLS-OSPF packet family.
- `vip/` contains the control-plane NLS-VIP packet family.
- `payload/normal/` represents ordinary data-plane traffic that is not NLS-protected when policy permits it.
- `payload/encrypted/` represents the protected inner packet carried by an NLS-Secured-Packet.

## Wire-format rule

The architecture document currently marks NLS byte-level field layouts, exact sizes, packet type values and identification mechanisms as **reference required**. Therefore this package does not invent byte offsets, field widths, protocol numbers, or serialization rules.

Once the authoritative NLS specification is available, wire-level `serialize()` / `deserialize()` implementations and interoperability vectors can be added against that specification.
