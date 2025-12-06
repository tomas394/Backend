from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, patients, webhooks, medications, community, timeline, care_circle, ai_processing, chat

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(medications.router, prefix="/medical", tags=["medical"])
api_router.include_router(community.router, prefix="/community", tags=["community"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(care_circle.router, prefix="/circle", tags=["circle"])
api_router.include_router(ai_processing.router, prefix="/ai", tags=["ai"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
