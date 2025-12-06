# Import all the models, so that Base has them before being
# imported by Alembic or used for create_all
from app.models.user import User
from app.models.patient import Patient
from app.models.health_data import HealthMetric
from sqlmodel import SQLModel

# Re-export SQLModel as Base for convenience if needed,
# although SQLModel is usually enough.
Base = SQLModel
