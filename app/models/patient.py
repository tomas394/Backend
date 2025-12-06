from typing import Optional, List, Dict
from datetime import date
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB
from app.models.user import User

class PatientBase(SQLModel):
    full_name: str
    birth_date: date
    # Standardizing JSONB usage with sa_column
    care_plan_summary: Dict = Field(default={}, sa_column=Column(JSONB))
    family_manager_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Patient(PatientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    family_manager: Optional[User] = Relationship()

    # Relationships (Using string forward refs to avoid circular imports if needed later)
    # care_circle: List["CareCircleMember"] = Relationship(back_populates="patient")
    # medications: List["Medication"] = Relationship(back_populates="patient")
