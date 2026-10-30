"""Initialize the NLS secure key store."""
from __future__ import annotations
from pathlib import Path
import sys

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from router_os.crypto.secure_storage.secure_store import SecureStore


def initialize_key_store() -> SecureStore:
    """Return the configured secure store.

    Production deployments should replace SecureStore with a TPM/HSM/SE-backed
    implementation so secret material is non-exportable.
    """
    return SecureStore()
