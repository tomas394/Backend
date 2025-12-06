from typing import Optional, Dict
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class ServiceType(str, Enum):
    TRANSPORT = "TRANSPORT"
    SHOPPING = "SHOPPING"
    COMPANIONSHIP = "COMPANIONSHIP"

class RequestStatus(str, Enum):
    OPEN = "OPEN"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS" # "Voluntário a caminho"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ServiceRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    requester_id: int = Field(foreign_key="user.id")
    volunteer_id: Optional[int] = Field(default=None, foreign_key="user.id")

    service_type: ServiceType
    status: RequestStatus = Field(default=RequestStatus.OPEN)

    description: Optional[str] = None

    # Geo location logic (mocked as JSON)
    # e.g., {"lat": 38.7, "lon": -9.1, "address": "Rua X"}
    pickup_location: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))
    destination_location: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))

    scheduled_time: datetime
    estimated_arrival_minutes: Optional[int] = None # "7 min" dynamic field update

    created_at: datetime = Field(default_factory=datetime.utcnow)
