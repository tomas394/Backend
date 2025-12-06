import hmac
import hashlib
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, Header, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.core.config import settings
from app.schemas.webhook import WebhookPayload
# In a real app we might convert WebhookPayload to HealthMetric and store it
# from app.models.health_data import HealthMetric

router = APIRouter()

async def verify_terra_signature(
    request: Request,
    terra_signature: str = Header(None, alias="Terra-Signature")
):
    """
    Verifies the HMAC SHA-256 signature of the incoming request from Terra API.

    The signature is expected to be in the 'Terra-Signature' header.
    It is a hex digest of the body signed with the shared secret.
    """
    if not terra_signature:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing Terra-Signature header"
        )

    # Read the raw body
    body = await request.body()

    # Calculate expected signature
    # Ensure secret is bytes
    secret = settings.TERRA_WEBHOOK_SECRET.encode('utf-8')

    # Calculate HMAC SHA256
    expected_signature = hmac.new(
        secret,
        body,
        hashlib.sha256
    ).hexdigest()

    # Constant time comparison to prevent timing attacks
    if not hmac.compare_digest(expected_signature, terra_signature):
         # Log this security incident in real life
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid signature"
        )

    return True

@router.post("/terra", status_code=200)
async def terra_webhook(
    payload: WebhookPayload,
    request: Request,
    # Injecting the signature verification dependency.
    # Note: We use the dependency to validate, but we don't necessarily need the return value here.
    # The payload is already parsed by Pydantic *after* we read the body in the dependency?
    # Wait, FastAPI reads body for Pydantic. If we consume it in dependency, it might be consumed.
    # Actually, Request.body() is cached by Starlette/FastAPI so calling it multiple times is fine.
    authorized: bool = Depends(verify_terra_signature),
    session: AsyncSession = Depends(deps.get_session)
) -> Any:
    """
    Receive Health Data from Terra API.
    Validates HMAC signature before processing.
    """

    # Process payload (mock implementation)
    # In production:
    # 1. Parse payload.data
    # 2. Map to HealthMetric model
    # 3. Store in DB

    print(f"Received verified Terra webhook for User {payload.user_id} - Type: {payload.type}")

    return {"status": "ok"}
