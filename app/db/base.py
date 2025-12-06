# Import all the models, so that Base has them before being
# imported by Alembic or used for create_all
from app.models.user import User
from app.models.patient import Patient
# from app.models.health_data import HealthMetric # Might be redundant if we use medical.py, but keeping for safety if referenced elsewhere
from app.models.care_circle import CareCircleInvitation, CareCircleMember
from app.models.medical import Medication, Prescription, MedicationLog, HealthEvent
from app.models.community import ServiceRequest
from sqlmodel import SQLModel

# Re-export SQLModel as Base for convenience if needed,
# although SQLModel is usually enough.
Base = SQLModel
