from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CAREGIVER = "CAREGIVER"
    FAMILY = "FAMILY"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    role: UserRole = UserRole.FAMILY

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
