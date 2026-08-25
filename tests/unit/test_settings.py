from __future__ import annotations

from pathlib import Path

import pytest

from secureflow.settings import Settings


def clear_secureflow_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "SECUREFLOW_ENV",
        "SECUREFLOW_DB_PATH",
        "SECUREFLOW_SECRET",
        "SECUREFLOW_COOKIE_SECURE",
        "SECUREFLOW_SEED_DEMO_USERS",
        "SECUREFLOW_SESSION_TTL_SECONDS",
    ):
        monkeypatch.delenv(name, raising=False)


def test_development_generates_ephemeral_secret(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_secureflow_env(monkeypatch)
    monkeypatch.setenv("SECUREFLOW_DB_PATH", str(tmp_path / "dev.db"))

    with pytest.warns(RuntimeWarning, match="ephemeral local-only secret"):
        settings = Settings.from_env()

    assert settings.environment == "development"
    assert len(settings.secret) >= 32
    assert settings.cookie_secure is False
    assert settings.seed_demo_users is True


def test_production_requires_explicit_secret(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_secureflow_env(monkeypatch)
    monkeypatch.setenv("SECUREFLOW_ENV", "production")
    monkeypatch.setenv("SECUREFLOW_DB_PATH", str(tmp_path / "prod.db"))

    with pytest.raises(RuntimeError, match="SECUREFLOW_SECRET is required"):
        Settings.from_env()


def test_production_defaults_to_secure_cookie_and_no_demo_users(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    clear_secureflow_env(monkeypatch)
    monkeypatch.setenv("SECUREFLOW_ENV", "production")
    monkeypatch.setenv("SECUREFLOW_DB_PATH", str(tmp_path / "prod.db"))
    monkeypatch.setenv("SECUREFLOW_SECRET", "x" * 32)

    settings = Settings.from_env()

    assert settings.cookie_secure is True
    assert settings.seed_demo_users is False
