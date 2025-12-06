from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api import deps
from app.models.user import User
from app.models.community import ServiceRequest, RequestStatus
from app.schemas.community import ServiceRequestCreate, ServiceRequestRead
from app.services.matching import matching_service

router = APIRouter()

@router.post("/requests", response_model=ServiceRequestRead)
async def create_service_request(
    *,
    session: AsyncSession = Depends(deps.get_session),
    request_in: ServiceRequestCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Creates a new volunteer request (Uber-style).
    """
    request = ServiceRequest(
        patient_id=request_in.patient_id,
        requester_id=current_user.id, # The user asking for help
        service_type=request_in.service_type,
        description=request_in.description,
        pickup_location=request_in.pickup_location,
        destination_location=request_in.destination_location,
        scheduled_time=request_in.scheduled_time,
        status=RequestStatus.OPEN
    )
    session.add(request)
    await session.commit()
    await session.refresh(request)

    # Try to find a volunteer (Async background task in real life)
    # matching_service.find_volunteer(...)

    return request

@router.get("/{patient_id}", response_model=List[ServiceRequestRead])
async def read_requests(
    patient_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    List active service requests.
    """
    result = await session.exec(select(ServiceRequest).where(ServiceRequest.patient_id == patient_id))
    return result.all()
