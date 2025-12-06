from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api import deps
from app.core import security
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def read_users(
    session: AsyncSession = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve users.
    """
    result = await session.exec(select(User).offset(skip).limit(limit))
    users = result.all()
    return users

@router.post("/", response_model=UserResponse)
async def create_user(
    *,
    session: AsyncSession = Depends(deps.get_session),
    user_in: UserCreate,
    # Open registration for now, or restrict to Admin
) -> Any:
    """
    Create new user.
    """
    result = await session.exec(select(User).where(User.email == user_in.email))
    user = result.first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        role=user_in.role,
        is_active=user_in.is_active,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
