from fastapi import APIRouter
from app.api.v1 import social_media

api_router_social_media = APIRouter()

# Include all Social Media endpoints
api_router_social_media.include_router(social_media.router, prefix="/social-media", tags=["social-media"])
