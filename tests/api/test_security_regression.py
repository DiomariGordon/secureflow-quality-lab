from __future__ import annotations

import pytest


@pytest.mark.security
def test_missing_csrf_token_blocks_state_change(client):
    login = client.post(
        "/api/auth/login",
        json={"email": "analyst.one@example.test", "password": "AnalystPass!1"},
    )
    assert login.status_code == 200
    response = client.post(
        "/api/records",
        json={"title": "Blocked write", "description": "No CSRF token", "risk_score": 10},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "CSRF validation failed"


@pytest.mark.security
def test_viewer_cannot_create_record(viewer_session):
    client, headers = viewer_session
    response = client.post(
        "/api/records",
        headers=headers,
        json={"title": "Unauthorized", "description": "Viewer write attempt", "risk_score": 20},
    )
    assert response.status_code == 403


@pytest.mark.security
def test_horizontal_access_is_blocked(client):
    login_one = client.post(
        "/api/auth/login",
        json={"email": "analyst.one@example.test", "password": "AnalystPass!1"},
    )
    csrf_one = login_one.json()["csrf_token"]
    created = client.post(
        "/api/records",
        headers={"X-CSRF-Token": csrf_one},
        json={"title": "Private record", "description": "Owned by analyst one", "risk_score": 65},
    )
    record_id = created.json()["id"]

    client.cookies.clear()
    login_two = client.post(
        "/api/auth/login",
        json={"email": "analyst.two@example.test", "password": "AnalystPass!2"},
    )
    assert login_two.status_code == 200
    denied = client.get(f"/api/records/{record_id}")
    assert denied.status_code == 403
    assert denied.json()["detail"] == "Record access denied"


@pytest.mark.security
def test_logout_invalidates_server_side_session(client):
    login = client.post(
        "/api/auth/login",
        json={"email": "analyst.one@example.test", "password": "AnalystPass!1"},
    )
    csrf = login.json()["csrf_token"]
    token = client.cookies.get("secureflow_session")
    assert token

    logout = client.post("/api/auth/logout", headers={"X-CSRF-Token": csrf})
    assert logout.status_code == 204

    client.cookies.set("secureflow_session", token)
    denied = client.get("/api/auth/me")
    assert denied.status_code == 401
    assert denied.json()["detail"] == "Inactive session"


@pytest.mark.security
def test_security_headers_and_cookie_attributes(client):
    page = client.get("/")
    assert page.status_code == 200
    assert page.headers["x-content-type-options"] == "nosniff"
    assert page.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in page.headers["content-security-policy"]

    login = client.post(
        "/api/auth/login",
        json={"email": "analyst.one@example.test", "password": "AnalystPass!1"},
    )
    set_cookie = login.headers["set-cookie"].lower()
    assert "httponly" in set_cookie
    assert "samesite=strict" in set_cookie
