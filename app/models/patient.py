from typing import Optional, List, Dict
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.user import User

class PatientBase(SQLModel):
    full_name: str
    birth_date: date
    # Using JSONB as requested in the prompt ("JSONB" for care_plan_summary)
    care_plan_summary: Dict = Field(default={}, sa_type=JSONB)
    family_manager_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Patient(PatientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    family_manager: Optional[User] = Relationship()
    # health_metrics: List["HealthMetric"] = Relationship(back_populates="patient")
