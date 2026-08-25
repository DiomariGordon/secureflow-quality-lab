from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException, Request, status

from .db import Database, utc_now_iso, verify_password
from .settings import Settings

SESSION_COOKIE = "secureflow_session"
CSRF_HEADER = "X-CSRF-Token"


@dataclass(frozen=True)
class AuthenticatedUser:
    id: int
    email: str
    display_name: str
    role: str
    session_id: str
    csrf_token: str


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def sign_session(session_id: str, secret: str) -> str:
    """Return an integrity-protected session reference.

    Learning anchor: HMAC lets the server detect tampering. It does not encrypt
    the payload, which is why only an opaque session identifier is included.
    """
    payload = json.dumps({"sid": session_id}, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).digest()
    return f"{_b64encode(payload)}.{_b64encode(signature)}"


def verify_session_signature(token: str, secret: str) -> str | None:
    try:
        encoded_payload, encoded_signature = token.split(".", 1)
        payload = _b64decode(encoded_payload)
        signature = _b64decode(encoded_signature)
        expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            return None
        data: dict[str, Any] = json.loads(payload.decode("utf-8"))
        session_id = data.get("sid")
        return session_id if isinstance(session_id, str) else None
    except (ValueError, binascii.Error, json.JSONDecodeError, UnicodeDecodeError):
        return None


def authenticate_credentials(db: Database, email: str, password: str):
    with db.connect() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE lower(email) = lower(?) AND active = 1",
            (email.strip(),),
        ).fetchone()
    if row is None:
        return None
    if not verify_password(password, row["password_salt"], row["password_hash"]):
        return None
    return row


def create_session(db: Database, user_id: int, ttl_seconds: int) -> tuple[str, str]:
    session_id = secrets.token_urlsafe(32)
    csrf_token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(UTC) + timedelta(seconds=ttl_seconds)).isoformat()
    with db.connect() as connection:
        connection.execute(
            """
            INSERT INTO sessions (id, user_id, csrf_token, expires_at, active, created_at)
            VALUES (?, ?, ?, ?, 1, ?)
            """,
            (session_id, user_id, csrf_token, expires_at, utc_now_iso()),
        )
    return session_id, csrf_token


def get_authenticated_user(
    request: Request,
    db: Database,
    settings: Settings,
    *,
    require_csrf: bool = False,
) -> AuthenticatedUser:
    # Authentication succeeds only after two independent checks: the cookie
    # signature is valid and the referenced server-side session is active.
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    session_id = verify_session_signature(token, settings.secret)
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")

    with db.connect() as connection:
        row = connection.execute(
            """
            SELECT
                s.id AS session_id,
                s.csrf_token,
                s.expires_at,
                s.active AS session_active,
                u.id AS user_id,
                u.email,
                u.display_name,
                u.role,
                u.active AS user_active
            FROM sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.id = ?
            """,
            (session_id,),
        ).fetchone()

    if row is None or not row["session_active"] or not row["user_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive session")
    if datetime.fromisoformat(row["expires_at"]) <= datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired session")

    if require_csrf:
        # State-changing cookie-authenticated requests require a second value
        # an attacker cannot cause a victim browser to send automatically.
        supplied = request.headers.get(CSRF_HEADER)
        if not supplied or not hmac.compare_digest(supplied, row["csrf_token"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF validation failed")

    return AuthenticatedUser(
        id=row["user_id"],
        email=row["email"],
        display_name=row["display_name"],
        role=row["role"],
        session_id=row["session_id"],
        csrf_token=row["csrf_token"],
    )


def invalidate_session(db: Database, session_id: str) -> None:
    with db.connect() as connection:
        connection.execute("UPDATE sessions SET active = 0 WHERE id = ?", (session_id,))
