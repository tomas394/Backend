from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CAREGIVER = "CAREGIVER" # Professional? Or Family?
    # As per prompt requirements:
    FAMILY = "FAMILY"
    PRO = "PRO"
    VOLUNTEER = "VOLUNTEER"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    role: UserRole = UserRole.FAMILY
    # UI: Check verde para voluntários verificados
    is_verified: bool = Field(default=False)
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
