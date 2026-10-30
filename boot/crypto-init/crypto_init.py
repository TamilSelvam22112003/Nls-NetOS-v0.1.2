"""NLS cryptographic subsystem boot initialization."""
from __future__ import annotations

from pathlib import Path
import sys

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from router_os.crypto.key_management.key_manager import KeyManager
from router_os.crypto.secure_storage.secure_store import SecureStore


def initialize_crypto() -> None:
    """Initialize secure hardware/storage and ensure required NLS keys."""
    from secure_hardware_init import initialize_secure_hardware
    from key_store_init import initialize_key_store

    initialize_secure_hardware()
    store = initialize_key_store()
    manager = KeyManager(store)
    manager.ensure_synchronous()
    manager.ensure_asymmetric_identity()


if __name__ == "__main__":
    initialize_crypto()
