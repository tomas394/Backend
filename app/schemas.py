from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
import enum

class UserRole(str, enum.Enum):
    family_admin = "family_admin"
    professional = "professional"
    volunteer = "volunteer"
    municipality = "municipality"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str]
    role: UserRole
    phone: Optional[str]
    is_verified_volunteer: Optional[bool] = False
    municipality_id: Optional[str]

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class PatientBase(BaseModel):
    name: str
    address: Optional[str]
    birth_date: Optional[date]

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: int
    manager_id: int

    class Config:
        orm_mode = True

class EventType(str, enum.Enum):
    medical = "medical"
    social = "social"
    transport = "transport"

class EventStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"

class EventBase(BaseModel):
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    type: EventType
    is_municipal_request: Optional[bool] = False
    geo_lat: Optional[float]
    geo_long: Optional[float]

class EventCreate(EventBase):
    patient_id: int
    request_municipal_help: Optional[bool] = False

class EventOut(EventBase):
    id: int
    status: EventStatus
    volunteer_id: Optional[int]
    patient_id: int

    class Config:
        orm_mode = True

class HealthMetricType(str, enum.Enum):
    heart_rate = "heart_rate"
    steps = "steps"
    sleep = "sleep"

class HealthMetricBase(BaseModel):
    metric_type: HealthMetricType
    value: float
    timestamp: datetime

class HealthMetricCreate(HealthMetricBase):
    patient_id: int

class HealthMetricOut(HealthMetricBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True