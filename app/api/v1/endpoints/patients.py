from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api import deps
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate

router = APIRouter()

@router.get("/", response_model=List[PatientResponse])
async def read_patients(
    session: AsyncSession = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve patients.
    """
    # Simple logic: return all if Admin, else filter?
    # For scaffold, return all.
    result = await session.exec(select(Patient).offset(skip).limit(limit))
    patients = result.all()
    return patients

@router.post("/", response_model=PatientResponse)
async def create_patient(
    *,
    session: AsyncSession = Depends(deps.get_session),
    patient_in: PatientCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new patient.
    """
    patient = Patient.model_validate(patient_in)
    session.add(patient)
    await session.commit()
    await session.refresh(patient)
    return patient
