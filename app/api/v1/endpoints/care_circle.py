from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api import deps
from app.models.user import User
from app.models.care_circle import CareCircleInvitation, InvitationStatus
from app.schemas.care_circle import CareCircleInvitationCreate, CareCircleInvitationRead
from app.services.notification import notification_service

router = APIRouter()

@router.post("/invite", response_model=CareCircleInvitationRead)
async def invite_member(
    *,
    session: AsyncSession = Depends(deps.get_session),
    invite_in: CareCircleInvitationCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Invite a new member (Family, Pro, Volunteer) to the Circle.
    """
    # Check if already pending
    result = await session.exec(select(CareCircleInvitation).where(
        CareCircleInvitation.email == invite_in.email,
        CareCircleInvitation.patient_id == invite_in.patient_id,
        CareCircleInvitation.status == InvitationStatus.PENDING
    ))
    if result.first():
        raise HTTPException(status_code=400, detail="Invitation already pending.")

    invitation = CareCircleInvitation(
        email=invite_in.email,
        patient_id=invite_in.patient_id,
        invited_by_id=current_user.id,
        status=InvitationStatus.PENDING
    )
    session.add(invitation)
    await session.commit()
    await session.refresh(invitation)

    # Send Email/SMS
    notification_service.send_email(invite_in.email, "Invitation to Care Circle", "You have been invited...")

    return invitation
