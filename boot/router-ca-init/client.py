"""Boot-time Router-CA client activation wrapper."""


def activate_client(config):
    return {"provider_selection": config.get("provider_selection", "recommended")}
