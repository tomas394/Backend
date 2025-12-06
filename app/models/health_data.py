from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.models.patient import Patient

class HealthMetricBase(SQLModel):
    patient_id: int = Field(foreign_key="patient.id")
    type: str # e.g. "heart_rate", "steps"
    value: float
    timestamp: datetime
    source_device: Optional[str] = None

class HealthMetric(HealthMetricBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    patient: Optional[Patient] = Relationship()
