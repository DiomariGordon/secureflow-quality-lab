from __future__ import annotations

from sqlite3 import Row

from .db import Database, utc_now_iso


def classify_risk(score: int) -> str:
    """Classify a score using explicit requirement boundaries.

    Learning anchor: this is deliberately pure, making 39/40 and 69/70
    boundary behavior fast and deterministic to test.
    """
    if score < 40:
        return "LOW"
    if score < 70:
        return "MEDIUM"
    return "HIGH"


def log_audit(
    db: Database,
    *,
    event_type: str,
    actor_user_id: int | None,
    outcome: str,
    details: str,
    target_type: str | None = None,
    target_id: str | None = None,
) -> None:
    with db.connect() as connection:
        connection.execute(
            """
            INSERT INTO audit_events (
                event_type, actor_user_id, target_type, target_id,
                outcome, details, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_type,
                actor_user_id,
                target_type,
                target_id,
                outcome,
                details,
                utc_now_iso(),
            ),
        )


def create_record(
    db: Database,
    *,
    title: str,
    description: str,
    risk_score: int,
    owner_id: int,
) -> Row:
    now = utc_now_iso()
    risk_class = classify_risk(risk_score)
    with db.connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO records (
                title, description, risk_score, risk_class, status,
                owner_id, approved_by, created_at, updated_at
            ) VALUES (?, ?, ?, ?, 'DRAFT', ?, NULL, ?, ?)
            """,
            (title.strip(), description.strip(), risk_score, risk_class, owner_id, now, now),
        )
        row = connection.execute(
            "SELECT * FROM records WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    assert row is not None
    return row


def get_record(db: Database, record_id: int) -> Row | None:
    with db.connect() as connection:
        return connection.execute(
            "SELECT * FROM records WHERE id = ?", (record_id,)
        ).fetchone()


def list_records(db: Database, *, user_id: int, role: str) -> list[Row]:
    with db.connect() as connection:
        if role == "approver":
            rows = connection.execute(
                "SELECT * FROM records ORDER BY id DESC"
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM records WHERE owner_id = ? ORDER BY id DESC",
                (user_id,),
            ).fetchall()
    return list(rows)


def transition_record(
    db: Database,
    *,
    record_id: int,
    expected_status: str,
    new_status: str,
    approver_id: int | None = None,
) -> Row | None:
    # The expected-status predicate makes the transition conditional in the
    # database itself. A stale client cannot silently overwrite newer state.
    now = utc_now_iso()
    with db.connect() as connection:
        cursor = connection.execute(
            """
            UPDATE records
            SET status = ?, approved_by = COALESCE(?, approved_by), updated_at = ?
            WHERE id = ? AND status = ?
            """,
            (new_status, approver_id, now, record_id, expected_status),
        )
        if cursor.rowcount != 1:
            return None
        return connection.execute(
            "SELECT * FROM records WHERE id = ?", (record_id,)
        ).fetchone()


def list_audit_events(db: Database, limit: int = 100) -> list[Row]:
    with db.connect() as connection:
        rows = connection.execute(
            "SELECT * FROM audit_events ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return list(rows)
