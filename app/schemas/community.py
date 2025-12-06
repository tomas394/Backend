from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel
from app.models.community import ServiceType, RequestStatus

class ServiceRequestBase(BaseModel):
    service_type: ServiceType
    description: Optional[str] = None
    pickup_location: Optional[Dict] = None
    destination_location: Optional[Dict] = None
    scheduled_time: datetime

class ServiceRequestCreate(ServiceRequestBase):
    patient_id: int

class ServiceRequestRead(ServiceRequestBase):
    id: int
    patient_id: int
    requester_id: int
    volunteer_id: Optional[int] = None
    status: RequestStatus
    estimated_arrival_minutes: Optional[int] = None
