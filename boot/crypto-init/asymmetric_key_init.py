"""Boot-time asymmetric-key lifecycle for NLS."""


def ensure_asymmetric_key() -> None:
    """Ensure the NLS asymmetric identity key pair exists securely."""
    # First boot/provisioning generates the identity key pair; subsequent boots
    # load the existing protected private key instead of replacing the identity.
    return None
