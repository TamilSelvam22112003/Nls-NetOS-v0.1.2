"""Router-CA boot activation entry point."""
from config import load_router_ca_config
from database import initialize_router_ca_database
from provider_loader import load_recommended_providers
from certificate_loader import load_certificates
from trust_loader import load_trust
from key_state_loader import load_key_state
from health_check import check_router_ca_health


def activate_router_ca():
    config = load_router_ca_config()
    if not config.get("enabled", False):
        return {"status": "disabled"}
    initialize_router_ca_database(config)
    load_recommended_providers(config)
    load_certificates(config)
    load_trust(config)
    load_key_state(config)
    health = check_router_ca_health(config)
    return {"status": "active", "health": health}
