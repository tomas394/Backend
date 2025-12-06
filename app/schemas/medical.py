from typing import Optional, List
from datetime import date
from pydantic import BaseModel
from app.models.medical import MedicationStatus

class MedicationBase(BaseModel):
    name: str
    dosage: str
    instructions: str
    is_active: bool = True

class MedicationCreate(MedicationBase):
    patient_id: int

class MedicationUpdate(MedicationBase):
    pass

class MedicationRead(MedicationBase):
    id: int
    patient_id: int

# AI "Human-in-the-Loop" Draft
class MedicationDraft(BaseModel):
    """
    Temporary object returned by OCR service.
    Not saved to DB until confirmed.
    """
    name_detected: str
    dosage_detected: Optional[str] = None
    instructions_detected: Optional[str] = None
    confidence_score: float
    original_text: Optional[str] = None
