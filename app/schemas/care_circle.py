from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.care_circle import InvitationStatus

class CareCircleInvitationCreate(BaseModel):
    email: EmailStr
    patient_id: int

class CareCircleInvitationRead(BaseModel):
    id: int
    email: str
    status: InvitationStatus
    patient_id: int
    invited_by_id: int
    created_at: datetime
