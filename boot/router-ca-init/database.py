"""Router-CA persistent storage abstraction."""

from pathlib import Path
import sqlite3

from .schema import SCHEMA_SQL


class RouterCADatabase:
    """Local persistent metadata store for Router-CA trust anchors.

    The database may live on persistent flash/eMMC/NVRAM. It is not a secret
    store and therefore never contains private key material directly.
    """

    def __init__(self, path: str = "/var/lib/nls/router-ca.db") -> None:
        self.path = Path(path)
        self.connection: sqlite3.Connection | None = None

    def open(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        # The SQL schema uses MySQL-specific ENUM/TIMESTAMP syntax, so the
        # runtime SQLite bootstrap is kept intentionally small and portable.
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS router_ca_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alias TEXT NOT NULL UNIQUE,
            ca_identifier TEXT NOT NULL UNIQUE,
            group_name TEXT,
            source_type TEXT NOT NULL DEFAULT 'other',
            enabled INTEGER NOT NULL DEFAULT 1,
            explicitly_untrusted INTEGER NOT NULL DEFAULT 0,
            enrollment_protocol TEXT NOT NULL DEFAULT 'none',
            enrollment_url TEXT,
            enrollment_auth_ref TEXT,
            bootstrap_token_ref TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS router_ca_certificate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            certificate_format TEXT NOT NULL,
            certificate_blob BLOB NOT NULL,
            public_key_blob BLOB,
            public_key_algorithm TEXT,
            public_key_bits INTEGER,
            ski BLOB,
            fingerprint_sha256 BLOB NOT NULL UNIQUE,
            fingerprint_sha512 BLOB,
            subject_dn TEXT NOT NULL,
            issuer_dn TEXT NOT NULL,
            serial_number TEXT NOT NULL,
            not_before TEXT NOT NULL,
            not_after TEXT NOT NULL,
            signature_algorithm TEXT,
            is_trust_anchor INTEGER NOT NULL DEFAULT 1,
            active INTEGER NOT NULL DEFAULT 1,
            revoked INTEGER NOT NULL DEFAULT 0,
            installed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(profile_id) REFERENCES router_ca_profile(id)
        );
        CREATE TABLE IF NOT EXISTS router_ca_sync_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL UNIQUE,
            endpoint TEXT NOT NULL,
            last_success_at TEXT,
            last_attempt_at TEXT,
            next_refresh_at TEXT,
            last_error TEXT,
            remote_version TEXT,
            state TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY(profile_id) REFERENCES router_ca_profile(id)
        );
        """)
        self.connection.commit()

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None
