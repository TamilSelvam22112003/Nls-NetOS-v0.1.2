# Database and migrations

SQLite is the initial development target for control-plane state, using explicit transaction boundaries and versioned migrations. Do not store private keys or traffic keys in plaintext tables.

Planned schema domains: NLS VIP, trust, LSDB, neighbor, adjacency, key/session metadata, synchronization, OSPF integration state, and Router-CA registry.

MySQL is not required for the first prototype; a later backend should implement the same repository interfaces and transaction expectations.
