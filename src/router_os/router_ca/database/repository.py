"""Persistence interface for Router-CA metadata and lifecycle state."""

class RouterCARepository:
    def __init__(self, connection):
        self.connection = connection

    def get_due_refreshes(self):
        raise NotImplementedError

    def get_active_router_ca(self):
        raise NotImplementedError

    def update_lifecycle_state(self, router_ca_id, status):
        raise NotImplementedError
