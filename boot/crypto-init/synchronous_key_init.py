"""Boot-time synchronous-key lifecycle for NLS."""
from __future__ import annotations
from pathlib import Path
import sys

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from router_os.crypto.key_management.key_manager import KeyManager
from router_os.crypto.secure_storage.secure_store import SecureStore


def ensure_synchronous_key(store: SecureStore | None = None):
    """Load the active synchronous key or generate it on first initialization."""
    return KeyManager(store).ensure_synchronous()
