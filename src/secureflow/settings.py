from __future__ import annotations

import os
import secrets
import warnings
from dataclasses import dataclass
from pathlib import Path


def _parse_bool(name: str, value: str | None, *, default: bool) -> bool:
    """Parse a strict boolean environment variable.

    Rejecting unknown values avoids silently treating misspellings such as
    ``treu`` as ``False`` in a security-sensitive configuration.
    """
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value")


@dataclass(frozen=True)
class Settings:
    db_path: Path
    secret: str
    cookie_secure: bool = False
    session_ttl_seconds: int = 60 * 60
    environment: str = "development"
    seed_demo_users: bool = True

    @classmethod
    def from_env(cls) -> "Settings":
        environment = os.getenv("SECUREFLOW_ENV", "development").strip().lower()
        if environment not in {"development", "test", "production"}:
            raise ValueError(
                "SECUREFLOW_ENV must be one of: development, test, production"
            )

        db_path = Path(os.getenv("SECUREFLOW_DB_PATH", "./secureflow.db"))
        secret = os.getenv("SECUREFLOW_SECRET")
        if not secret:
            if environment == "production":
                raise RuntimeError(
                    "SECUREFLOW_SECRET is required when SECUREFLOW_ENV=production"
                )
            secret = secrets.token_urlsafe(48)
            warnings.warn(
                "SECUREFLOW_SECRET was not set; generated an ephemeral local-only "
                "secret. Existing sessions will be invalid after restart.",
                RuntimeWarning,
                stacklevel=2,
            )
        elif environment == "production" and len(secret) < 32:
            raise RuntimeError(
                "SECUREFLOW_SECRET must contain at least 32 characters in production"
            )

        cookie_secure = _parse_bool(
            "SECUREFLOW_COOKIE_SECURE",
            os.getenv("SECUREFLOW_COOKIE_SECURE"),
            default=environment == "production",
        )
        seed_demo_users = _parse_bool(
            "SECUREFLOW_SEED_DEMO_USERS",
            os.getenv("SECUREFLOW_SEED_DEMO_USERS"),
            default=environment != "production",
        )

        ttl_raw = os.getenv("SECUREFLOW_SESSION_TTL_SECONDS", str(60 * 60))
        try:
            session_ttl_seconds = int(ttl_raw)
        except ValueError as exc:
            raise ValueError(
                "SECUREFLOW_SESSION_TTL_SECONDS must be an integer"
            ) from exc
        if session_ttl_seconds <= 0:
            raise ValueError("SECUREFLOW_SESSION_TTL_SECONDS must be positive")

        if environment == "production":
            if not cookie_secure:
                raise RuntimeError(
                    "SECUREFLOW_COOKIE_SECURE must be true in production"
                )
            if seed_demo_users:
                raise RuntimeError(
                    "SECUREFLOW_SEED_DEMO_USERS must be false in production"
                )

        return cls(
            db_path=db_path,
            secret=secret,
            cookie_secure=cookie_secure,
            session_ttl_seconds=session_ttl_seconds,
            environment=environment,
            seed_demo_users=seed_demo_users,
        )
