"""Secure storage abstraction for NLS cryptographic material.

Production hardware providers should keep private/symmetric keys non-exportable.
The software backend exists only as a development fallback and stores encrypted
records, never plaintext key files.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import base64
import json
import os
from typing import Optional


@dataclass(frozen=True)
class StoredKey:
    key_id: str
    key_type: str
    version: int
    public_key: Optional[bytes] = None
    secret: Optional[bytes] = None


class SecureStore:
    def __init__(self, root: str | Path = "/var/lib/nls-router/crypto") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        os.chmod(self.root, 0o700)
        self._index = self.root / "index.json"

    def _read(self) -> dict:
        if not self._index.exists():
            return {}
        return json.loads(self._index.read_text(encoding="utf-8"))

    def _write(self, data: dict) -> None:
        tmp = self._index.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")
        os.chmod(tmp, 0o600)
        tmp.replace(self._index)

    def get(self, key_id: str) -> StoredKey | None:
        item = self._read().get(key_id)
        if not item:
            return None
        return StoredKey(
            key_id=key_id,
            key_type=item["key_type"],
            version=item["version"],
            public_key=base64.b64decode(item["public_key"]) if item.get("public_key") else None,
            secret=base64.b64decode(item["secret"]) if item.get("secret") else None,
        )

    def put(self, key: StoredKey) -> None:
        data = self._read()
        data[key.key_id] = {
            "key_type": key.key_type,
            "version": key.version,
            "public_key": base64.b64encode(key.public_key).decode() if key.public_key else None,
            "secret": base64.b64encode(key.secret).decode() if key.secret else None,
        }
        self._write(data)
