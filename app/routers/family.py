from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import models, schemas, database
from ..services.ai_service import AIService, mock_ocr

router = APIRouter(prefix="/family", tags=["family"])

@router.post("/patients", response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(database.get_db), user_id: int = 1):
    db_patient = models.Patient(**patient.dict(), manager_id=user_id)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.post("/events", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    """
    Cria um evento. Se 'request_municipal_help' for True, envia para a Câmara.
    """
    is_municipal = event.request_municipal_help or event.is_municipal_request
    db_event = models.Event(
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        location=event.location,
        type=event.type,
        is_municipal_request=is_municipal,
        status=models.EventStatus.pending,
        geo_lat=event.geo_lat,
        geo_long=event.geo_long,
        patient_id=event.patient_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.post("/ocr/upload")
def ocr_upload(file: UploadFile = File(...)):
    """
    Recebe foto da receita e retorna dados extraídos.
    """
    # Mock OCR
    result = mock_ocr(file)
    return result