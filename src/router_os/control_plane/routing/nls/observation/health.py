"""NLS network observation health."""
class HealthMonitor:
    def check(self, inventory):
        return {"interfaces": len(inventory.interfaces), "healthy": True}
