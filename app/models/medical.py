from typing import Optional, List
from enum import Enum
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship

class MedicationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

class LogStatus(str, Enum):
    TAKEN = "TAKEN"
    MISSED = "MISSED"
    SKIPPED = "SKIPPED"

class Medication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")

    name: str
    dosage: str # "5mg"
    instructions: str # "ao jantar"
    is_active: bool = Field(default=True)

    # Relationships
    # Using string forward references to avoid circular import issues
    logs: List["MedicationLog"] = Relationship(back_populates="medication")

class Prescription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    medication_id: int = Field(foreign_key="medication.id")

    expiration_date: date # "Renovável até"
    pharmacy_name: Optional[str] = None
    photo_url: Optional[str] = None # digitalizada

    # Relationships can be added if we add a back_populates on Medication

class MedicationLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    medication_id: int = Field(foreign_key="medication.id")
    patient_id: int = Field(foreign_key="patient.id")

    status: LogStatus
    administered_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

    medication: Optional[Medication] = Relationship(back_populates="logs")

class HealthEvent(SQLModel, table=True):
    """
    General health events for the timeline (Visitas, Consultas, etc.)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")

    title: str
    description: Optional[str] = None
    event_type: str # "APPOINTMENT", "VISIT", "ALERT"
    start_time: datetime
    end_time: Optional[datetime] = None
    created_by_id: Optional[int] = Field(foreign_key="user.id")
