from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from secureflow.app import create_app
from secureflow.settings import Settings


@pytest.fixture()
def settings(tmp_path: Path) -> Settings:
    return Settings(
        db_path=tmp_path / "test.db",
        secret="test-secret-that-is-long-enough-for-the-lab",
        cookie_secure=False,
        session_ttl_seconds=300,
    )


@pytest.fixture()
def app(settings: Settings):
    return create_app(settings)


@pytest.fixture()
def client(app):
    with TestClient(app) as test_client:
        yield test_client


def login(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["csrf_token"]


@pytest.fixture()
def analyst_session(client: TestClient):
    csrf = login(client, "analyst.one@example.test", "AnalystPass!1")
    return client, {"X-CSRF-Token": csrf}


@pytest.fixture()
def viewer_session(client: TestClient):
    csrf = login(client, "viewer@example.test", "ViewerPass!1")
    return client, {"X-CSRF-Token": csrf}


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture(scope="session")
def live_server_url(tmp_path_factory: pytest.TempPathFactory):
    port = _free_port()
    db_path = tmp_path_factory.mktemp("live-server") / "e2e.db"
    env = os.environ.copy()
    env.update(
        {
            "SECUREFLOW_ENV": "test",
            "SECUREFLOW_DB_PATH": str(db_path),
            "SECUREFLOW_SECRET": "e2e-secret-that-is-long-enough-for-the-lab",
            "SECUREFLOW_COOKIE_SECURE": "false",
            "SECUREFLOW_SEED_DEMO_USERS": "true",
        }
    )
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "secureflow.app:create_app",
            "--factory",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            if httpx.get(f"{url}/health", timeout=0.5).status_code == 200:
                break
        except httpx.HTTPError:
            time.sleep(0.1)
    else:
        output = process.stdout.read() if process.stdout else ""
        process.terminate()
        raise RuntimeError(f"Live server did not start. Output:\n{output}")

    yield url
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
