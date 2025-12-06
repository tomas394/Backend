from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/b2g", tags=["b2g"])

@router.get("/feed", response_model=List[schemas.EventOut])
def municipal_feed(db: Session = Depends(database.get_db)):
    events = db.query(models.Event).filter(
        models.Event.is_municipal_request == True,
        models.Event.volunteer_id == None
    ).all()
    return events

@router.post("/accept/{event_id}")
def accept_task(event_id: int, db: Session = Depends(database.get_db), volunteer_id: int = 1):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event or not event.is_municipal_request:
        raise HTTPException(status_code=404, detail="Event not found or not municipal")
    if event.volunteer_id:
        raise HTTPException(status_code=400, detail="Already accepted")
    event.volunteer_id = volunteer_id
    event.status = models.EventStatus.accepted
    db.commit()
    db.refresh(event)
    return {"message": "Task accepted", "event_id": event.id}

@router.post("/tracking/{event_id}")
def update_tracking(event_id: int, geo_lat: float, geo_long: float, db: Session = Depends(database.get_db), volunteer_id: int = 1):
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.volunteer_id == volunteer_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found or not assigned to volunteer")
    event.geo_lat = geo_lat
    event.geo_long = geo_long
    event.status = models.EventStatus.in_progress
    db.commit()
    db.refresh(event)
    return {"message": "Tracking updated", "event_id": event.id}