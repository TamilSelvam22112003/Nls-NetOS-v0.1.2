# SQLite schema

Add numbered, reviewed SQL migrations before persistent state is used. Each schema change must define constraints, indices, migration behavior, rollback expectations, and concurrency tests. Avoid speculative production tables until entity semantics are frozen.
