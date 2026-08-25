from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

from .auth import (
    SESSION_COOKIE,
    authenticate_credentials,
    create_session,
    get_authenticated_user,
    invalidate_session,
    sign_session,
)
from .db import Database
from .models import (
    AuditEventResponse,
    LoginRequest,
    LoginResponse,
    RecordCreate,
    RecordResponse,
    UserResponse,
)
from .repository import (
    create_record,
    get_record,
    list_audit_events,
    list_records,
    log_audit,
    transition_record,
)
from .settings import Settings
from .ui import render_ui


def row_to_dict(row: Any) -> dict[str, Any]:
    return dict(row)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Compose the application boundary, dependencies, routes, and security controls.

    Learning anchor: this function is the composition root. It wires objects
    together; business rules remain in smaller modules so they can be tested
    without starting a browser or web server.
    """
    resolved = settings or Settings.from_env()
    db = Database(resolved.db_path)
    db.initialize(seed_demo_users=resolved.seed_demo_users)

    app = FastAPI(
        title="SecureFlow Quality Lab",
        version="0.3.0",
        description="Synthetic application for quality-engineering portfolio work.",
    )
    app.state.settings = resolved
    app.state.db = db

    @app.middleware("http")
    async def security_headers(request: Request, call_next: Callable):
        # Apply response controls centrally so a new route does not have to
        # remember each header independently. The later CSP milestone removes
        # the current inline-script/style exceptions.
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
        )
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(HTTPException)
    async def audit_http_exception(request: Request, exc: HTTPException):
        if exc.status_code in {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN}:
            log_audit(
                db,
                event_type="ACCESS_DECISION",
                actor_user_id=None,
                outcome="DENIED",
                details=f"{request.method} {request.url.path}: {exc.detail}",
            )
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.get("/", include_in_schema=False)
    def index():
        return render_ui()

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "secureflow-quality-lab"}

    @app.post("/api/auth/login", response_model=LoginResponse)
    def login(payload: LoginRequest, response: Response):
        user = authenticate_credentials(db, payload.email, payload.password)
        if user is None:
            log_audit(
                db,
                event_type="LOGIN",
                actor_user_id=None,
                outcome="FAILURE",
                details=f"Failed login for {payload.email.strip().lower()}",
            )
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # The cookie contains a signed session identifier, while active/expired
        # state remains on the server. Signing protects integrity, not secrecy.
        session_id, csrf_token = create_session(db, user["id"], resolved.session_ttl_seconds)
        response.set_cookie(
            key=SESSION_COOKIE,
            value=sign_session(session_id, resolved.secret),
            httponly=True,
            secure=resolved.cookie_secure,
            samesite="strict",
            max_age=resolved.session_ttl_seconds,
            path="/",
        )
        log_audit(
            db,
            event_type="LOGIN",
            actor_user_id=user["id"],
            outcome="SUCCESS",
            details="Session created",
        )
        return LoginResponse(
            user=UserResponse(
                id=user["id"],
                email=user["email"],
                display_name=user["display_name"],
                role=user["role"],
            ),
            csrf_token=csrf_token,
        )

    @app.post("/api/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
    def logout(request: Request, response: Response):
        user = get_authenticated_user(request, db, resolved, require_csrf=True)
        invalidate_session(db, user.session_id)
        response.delete_cookie(SESSION_COOKIE, path="/")
        response.status_code = status.HTTP_204_NO_CONTENT
        log_audit(
            db,
            event_type="LOGOUT",
            actor_user_id=user.id,
            outcome="SUCCESS",
            details="Session invalidated",
        )
        return response

    @app.get("/api/auth/me", response_model=UserResponse)
    def me(request: Request):
        user = get_authenticated_user(request, db, resolved)
        return UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            role=user.role,
        )

    @app.get("/api/records", response_model=list[RecordResponse])
    def records(request: Request):
        user = get_authenticated_user(request, db, resolved)
        return [RecordResponse(**row_to_dict(row)) for row in list_records(db, user_id=user.id, role=user.role)]

    @app.post("/api/records", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
    def add_record(payload: RecordCreate, request: Request):
        # Authentication establishes who is calling. This role check is the
        # separate authorization decision governing what that caller may do.
        user = get_authenticated_user(request, db, resolved, require_csrf=True)
        if user.role not in {"analyst", "approver"}:
            log_audit(
                db,
                event_type="CREATE_RECORD",
                actor_user_id=user.id,
                outcome="DENIED",
                details="Role is not allowed to create records",
            )
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role cannot create records")
        row = create_record(
            db,
            title=payload.title,
            description=payload.description,
            risk_score=payload.risk_score,
            owner_id=user.id,
        )
        log_audit(
            db,
            event_type="CREATE_RECORD",
            actor_user_id=user.id,
            target_type="record",
            target_id=str(row["id"]),
            outcome="SUCCESS",
            details=f"Created {row['risk_class']} risk record",
        )
        return RecordResponse(**row_to_dict(row))

    @app.get("/api/records/{record_id}", response_model=RecordResponse)
    def record_detail(record_id: int, request: Request):
        user = get_authenticated_user(request, db, resolved)
        row = get_record(db, record_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        # Horizontal authorization: a valid analyst session still cannot read
        # another analyst's record by changing the identifier in the URL.
        if user.role != "approver" and row["owner_id"] != user.id:
            log_audit(
                db,
                event_type="READ_RECORD",
                actor_user_id=user.id,
                target_type="record",
                target_id=str(record_id),
                outcome="DENIED",
                details="Horizontal authorization rule blocked access",
            )
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Record access denied")
        return RecordResponse(**row_to_dict(row))

    @app.post("/api/records/{record_id}/submit", response_model=RecordResponse)
    def submit_record(record_id: int, request: Request):
        user = get_authenticated_user(request, db, resolved, require_csrf=True)
        row = get_record(db, record_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        if user.role != "approver" and row["owner_id"] != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Record access denied")
        updated = transition_record(
            db,
            record_id=record_id,
            expected_status="DRAFT",
            new_status="SUBMITTED",
        )
        if updated is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Record is not in DRAFT status")
        log_audit(
            db,
            event_type="SUBMIT_RECORD",
            actor_user_id=user.id,
            target_type="record",
            target_id=str(record_id),
            outcome="SUCCESS",
            details="Record submitted for approval",
        )
        return RecordResponse(**row_to_dict(updated))

    @app.post("/api/records/{record_id}/approve", response_model=RecordResponse)
    def approve_record(record_id: int, request: Request):
        user = get_authenticated_user(request, db, resolved, require_csrf=True)
        if user.role != "approver":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Approver role required")
        updated = transition_record(
            db,
            record_id=record_id,
            expected_status="SUBMITTED",
            new_status="APPROVED",
            approver_id=user.id,
        )
        if updated is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Record is not in SUBMITTED status")
        log_audit(
            db,
            event_type="APPROVE_RECORD",
            actor_user_id=user.id,
            target_type="record",
            target_id=str(record_id),
            outcome="SUCCESS",
            details="Record approved",
        )
        return RecordResponse(**row_to_dict(updated))

    @app.get("/api/audit", response_model=list[AuditEventResponse])
    def audit(request: Request, limit: int = 100):
        user = get_authenticated_user(request, db, resolved)
        if user.role != "approver":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Approver role required")
        bounded_limit = min(max(limit, 1), 500)
        return [AuditEventResponse(**row_to_dict(row)) for row in list_audit_events(db, bounded_limit)]

    return app
