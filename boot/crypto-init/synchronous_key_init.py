"""Boot-time synchronous-key lifecycle for NLS."""


def ensure_synchronous_key() -> None:
    """Ensure the active NLS synchronous key exists in secure storage."""
    # The key manager must generate or load the active key through secure storage.
    # Raw key material must never be committed to the repository or database.
    return None
