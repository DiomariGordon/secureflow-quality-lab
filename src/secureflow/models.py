from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Role = Literal["viewer", "analyst", "approver"]
RecordStatus = Literal["DRAFT", "SUBMITTED", "APPROVED"]
RiskClass = Literal["LOW", "MEDIUM", "HIGH"]


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    email: str
    display_name: str
    role: Role


class LoginResponse(BaseModel):
    user: UserResponse
    csrf_token: str


class RecordCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=3, max_length=1000)
    risk_score: int = Field(ge=0, le=100)


class RecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    risk_score: int
    risk_class: RiskClass
    status: RecordStatus
    owner_id: int
    approved_by: int | None
    created_at: str
    updated_at: str


class AuditEventResponse(BaseModel):
    id: int
    event_type: str
    actor_user_id: int | None
    target_type: str | None
    target_id: str | None
    outcome: Literal["SUCCESS", "DENIED", "FAILURE"]
    details: str
    created_at: str
