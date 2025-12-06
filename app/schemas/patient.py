from typing import Optional, Dict
from datetime import date
from pydantic import BaseModel

class PatientBaseSchema(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    care_plan_summary: Optional[Dict] = None
    family_manager_id: Optional[int] = None

class PatientCreate(PatientBaseSchema):
    full_name: str
    birth_date: date
    family_manager_id: int

class PatientUpdate(PatientBaseSchema):
    pass

class PatientResponse(PatientBaseSchema):
    id: int

    class Config:
        from_attributes = True
