"""Route management boundary for NLS integration."""
class RouteManager:
    def __init__(self):
        self.routes = []

    def install(self, route):
        self.routes.append(route)
