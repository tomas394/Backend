from typing import Any, List, Dict
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api import deps
from app.models.user import User
from app.models.medical import HealthEvent, Medication
# from app.models.community import ServiceRequest

router = APIRouter()

@router.get("/{patient_id}/timeline")
async def get_patient_timeline(
    patient_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Dict[str, List[Any]]:
    """
    Aggregates data for the Dashboard Feed.
    Mixes Medication Schedules, Health Visits, and Alerts.
    """

    # 1. Get Health Events
    events_result = await session.exec(select(HealthEvent).where(HealthEvent.patient_id == patient_id))
    events = events_result.all()

    # 2. Get Medications (Simple logic: just listing them as "Daily" items)
    meds_result = await session.exec(select(Medication).where(Medication.patient_id == patient_id))
    meds = meds_result.all()

    # 3. Construct the feed
    # In a real app, we would generate specific "Task" instances for today based on the schedule.
    timeline_items = []

    for event in events:
        timeline_items.append({
            "type": "EVENT",
            "title": event.title,
            "time": event.start_time,
            "details": event.description
        })

    for med in meds:
        if med.is_active:
             timeline_items.append({
                "type": "MEDICATION",
                "title": f"Take {med.name}",
                "time": "09:00", # Mock time
                "details": f"{med.dosage} - {med.instructions}"
            })

    # Sort by time (Pseudo-sort for now as mix of datetime and string)
    # timeline_items.sort(key=lambda x: x['time'])

    return {"date": "2023-10-27", "items": timeline_items}
