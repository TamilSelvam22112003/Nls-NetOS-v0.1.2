"""Load Router-CA boot configuration."""

DEFAULT_CONFIG = {
    "enabled": True,
    "provider_selection": "recommended",
    "refresh_before_expiry_seconds": 2592000,
    "database_schema": "router_ca",
    "secure_key_backend": "tpm_or_hsm",
}


def load_router_ca_config():
    return DEFAULT_CONFIG.copy()
