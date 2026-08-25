from __future__ import annotations


def test_create_submit_approve_workflow(client):
    analyst_login = client.post(
        "/api/auth/login",
        json={"email": "analyst.one@example.test", "password": "AnalystPass!1"},
    )
    analyst_csrf = analyst_login.json()["csrf_token"]
    created = client.post(
        "/api/records",
        headers={"X-CSRF-Token": analyst_csrf},
        json={
            "title": "Release 24 readiness",
            "description": "Validate workflow, API, and data evidence.",
            "risk_score": 72,
        },
    )
    assert created.status_code == 201, created.text
    record = created.json()
    assert record["risk_class"] == "HIGH"
    assert record["status"] == "DRAFT"

    submitted = client.post(
        f"/api/records/{record['id']}/submit",
        headers={"X-CSRF-Token": analyst_csrf},
    )
    assert submitted.status_code == 200
    assert submitted.json()["status"] == "SUBMITTED"

    client.cookies.clear()
    approver_login = client.post(
        "/api/auth/login",
        json={"email": "approver@example.test", "password": "ApproverPass!1"},
    )
    approver_csrf = approver_login.json()["csrf_token"]
    approved = client.post(
        f"/api/records/{record['id']}/approve",
        headers={"X-CSRF-Token": approver_csrf},
    )
    assert approved.status_code == 200
    assert approved.json()["status"] == "APPROVED"
    assert approved.json()["approved_by"] == approver_login.json()["user"]["id"]

    audit = client.get("/api/audit")
    assert audit.status_code == 200
    event_types = {event["event_type"] for event in audit.json()}
    assert {"CREATE_RECORD", "SUBMIT_RECORD", "APPROVE_RECORD"}.issubset(event_types)


def test_risk_boundary_classification(analyst_session):
    client, headers = analyst_session
    scores = [(39, "LOW"), (40, "MEDIUM"), (69, "MEDIUM"), (70, "HIGH")]
    for score, expected in scores:
        response = client.post(
            "/api/records",
            headers=headers,
            json={
                "title": f"Boundary {score}",
                "description": "Boundary-value analysis",
                "risk_score": score,
            },
        )
        assert response.status_code == 201
        assert response.json()["risk_class"] == expected
