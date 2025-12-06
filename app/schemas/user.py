from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

# Shared properties
class UserBaseSchema(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = None

# Properties to receive via API on creation
class UserCreate(UserBaseSchema):
    email: EmailStr
    password: str
    role: UserRole

# Properties to receive via API on update
class UserUpdate(UserBaseSchema):
    password: Optional[str] = None

class UserInDBBase(UserBaseSchema):
    id: Optional[int] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class UserResponse(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
