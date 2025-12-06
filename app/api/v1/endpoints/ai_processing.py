from typing import Any
from fastapi import APIRouter, Depends, UploadFile, File
from app.api import deps
from app.models.user import User
from app.schemas.medical import MedicationDraft

router = APIRouter()

@router.post("/scan-document", response_model=MedicationDraft)
async def scan_document(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Simulates OCR processing for "Human-in-the-Loop" flow.
    Returns a Draft object that must be confirmed by the user.
    """
    # Simulate processing delay and logic
    # In production: Send to AWS Textract or Google Vision

    filename = file.filename
    print(f"Processing file: {filename}")

    # Mock result
    return MedicationDraft(
        name_detected="Ben-U-Ron",
        dosage_detected="500mg",
        instructions_detected="2x ao dia",
        confidence_score=0.95,
        original_text="Ben-U-Ron 500mg tomar 2x ao dia"
    )
