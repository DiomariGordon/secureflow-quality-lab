from __future__ import annotations


def test_api_result_matches_database_state(analyst_session, app):
    # Cross-layer oracle: the response is not trusted as proof of persistence.
    # The test independently reads SQLite and compares the committed state.
    client, headers = analyst_session
    response = client.post(
        "/api/records",
        headers=headers,
        json={
            "title": "Cross-layer verification",
            "description": "Compare API output to parameterized SQLite query.",
            "risk_score": 55,
        },
    )
    assert response.status_code == 201
    api_record = response.json()

    with app.state.db.connect() as connection:
        db_record = connection.execute(
            "SELECT * FROM records WHERE id = ?", (api_record["id"],)
        ).fetchone()

    assert db_record is not None
    assert db_record["title"] == api_record["title"]
    assert db_record["risk_score"] == api_record["risk_score"]
    assert db_record["risk_class"] == api_record["risk_class"]
    assert db_record["status"] == api_record["status"]
