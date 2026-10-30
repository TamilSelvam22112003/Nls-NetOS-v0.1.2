"""Boot-time asymmetric identity-key lifecycle for NLS."""
from __future__ import annotations
from pathlib import Path
import sys

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from router_os.crypto.key_management.key_manager import KeyManager
from router_os.crypto.secure_storage.secure_store import SecureStore


def ensure_asymmetric_key(store: SecureStore | None = None):
    """Load the existing identity or generate it only on first provisioning."""
    return KeyManager(store).ensure_asymmetric_identity()
