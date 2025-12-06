from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Float, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class UserRole(enum.Enum):
    family_admin = "family_admin"
    professional = "professional"
    volunteer = "volunteer"
    municipality = "municipality"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SqlEnum(UserRole), nullable=False)
    phone = Column(String)
    is_verified_volunteer = Column(Boolean, default=False)
    municipality_id = Column(String, nullable=True)
    patients = relationship("Patient", back_populates="manager")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    birth_date = Column(Date)
    manager_id = Column(Integer, ForeignKey("users.id"))
    manager = relationship("User", back_populates="patients")
    events = relationship("Event", back_populates="patient")
    health_metrics = relationship("HealthMetric", back_populates="patient")

class EventStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"

class EventType(enum.Enum):
    medical = "medical"
    social = "social"
    transport = "transport"

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    type = Column(SqlEnum(EventType), nullable=False)
    is_municipal_request = Column(Boolean, default=False)
    volunteer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(SqlEnum(EventStatus), default=EventStatus.pending)
    geo_lat = Column(Float, nullable=True)
    geo_long = Column(Float, nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="events")

class HealthMetricType(enum.Enum):
    heart_rate = "heart_rate"
    steps = "steps"
    sleep = "sleep"

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    metric_type = Column(SqlEnum(HealthMetricType), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime)
    patient = relationship("Patient", back_populates="health_metrics")