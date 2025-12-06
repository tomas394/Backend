from typing import Optional
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# Invitation Status
class InvitationStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class CareCircleInvitation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    status: InvitationStatus = Field(default=InvitationStatus.PENDING)
    patient_id: int = Field(foreign_key="patient.id")
    invited_by_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships could be added if needed

class CareCircleMember(SQLModel, table=True):
    """
    Link table between User and Patient with granular permissions.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    patient_id: int = Field(foreign_key="patient.id")

    # Permissions
    can_view_medication: bool = True
    can_manage_medication: bool = False
    can_view_health_data: bool = True
    can_coordinate_transport: bool = False

    role_label: Optional[str] = None # e.g. "Irmão", "Enfermeira Chefe"
