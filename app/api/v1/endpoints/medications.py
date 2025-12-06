from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api import deps
from app.models.user import User
from app.models.medical import Medication
from app.schemas.medical import MedicationCreate, MedicationRead, MedicationDraft

router = APIRouter()

@router.post("/events", response_model=MedicationRead)
async def confirm_medication_event(
    *,
    session: AsyncSession = Depends(deps.get_session),
    medication_in: MedicationCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Finalizes the 'Human-in-the-Loop' flow.
    Receives confirmed data (edited by user after AI draft) and saves to DB.
    """
    medication = Medication(
        name=medication_in.name,
        dosage=medication_in.dosage,
        instructions=medication_in.instructions,
        patient_id=medication_in.patient_id,
        is_active=medication_in.is_active
    )
    session.add(medication)
    await session.commit()
    await session.refresh(medication)

    # Trigger System Event in Chat (Mock)
    # chat_service.broadcast_system_event(f"New medication {medication.name} added by {current_user.email}")

    return medication

@router.get("/{patient_id}", response_model=List[MedicationRead])
async def read_medications(
    patient_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    List medications for a patient.
    """
    result = await session.exec(select(Medication).where(Medication.patient_id == patient_id))
    return result.all()
