from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas
from ..services.risk_engine import analyze_risk
from datetime import datetime

router = APIRouter(prefix="/webhooks", tags=["wearables"])

@router.post("/terra")
async def receive_wearable_data(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    metrics = data.get("data", [])
    risk_level = analyze_risk(metrics)
    for metric in metrics:
        new_metric = models.HealthMetric(
            patient_id=metric.get("patient_id", 1),
            metric_type=metric.get("type"),
            value=metric.get("value"),
            timestamp=datetime.now()
        )
        db.add(new_metric)
    db.commit()
    if risk_level == "HIGH":
        # Log warning (could be sent to alert system)
        print("[RISK WARNING] High risk detected for patient!")
    return {"status": "received", "risk": risk_level}