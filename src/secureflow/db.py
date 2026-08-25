from __future__ import annotations

import hashlib
import hmac
import os
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterator

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('viewer', 'analyst', 'approver')),
    password_salt BLOB NOT NULL,
    password_hash BLOB NOT NULL,
    active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    csrf_token TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0, 1)),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    risk_score INTEGER NOT NULL CHECK(risk_score BETWEEN 0 AND 100),
    risk_class TEXT NOT NULL CHECK(risk_class IN ('LOW', 'MEDIUM', 'HIGH')),
    status TEXT NOT NULL CHECK(status IN ('DRAFT', 'SUBMITTED', 'APPROVED')),
    owner_id INTEGER NOT NULL REFERENCES users(id),
    approved_by INTEGER REFERENCES users(id),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    actor_user_id INTEGER REFERENCES users(id),
    target_type TEXT,
    target_id TEXT,
    outcome TEXT NOT NULL CHECK(outcome IN ('SUCCESS', 'DENIED', 'FAILURE')),
    details TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

DEMO_USERS = (
    ("analyst.one@example.test", "Analyst One", "analyst", "AnalystPass!1"),
    ("analyst.two@example.test", "Analyst Two", "analyst", "AnalystPass!2"),
    ("viewer@example.test", "Read Only", "viewer", "ViewerPass!1"),
    ("approver@example.test", "Quality Approver", "approver", "ApproverPass!1"),
)


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=2**14,
        r=8,
        p=1,
        dklen=32,
    )


def verify_password(password: str, salt: bytes, expected_hash: bytes) -> bool:
    candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, expected_hash)


class Database:
    def __init__(self, path: Path):
        self.path = path

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self, *, seed_demo_users: bool = True) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)
            if not seed_demo_users:
                return
            for email, display_name, role, password in DEMO_USERS:
                exists = connection.execute(
                    "SELECT id FROM users WHERE email = ?", (email,)
                ).fetchone()
                if exists:
                    continue
                salt = os.urandom(16)
                connection.execute(
                    """
                    INSERT INTO users (
                        email, display_name, role, password_salt, password_hash
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (email, display_name, role, salt, hash_password(password, salt)),
                )
