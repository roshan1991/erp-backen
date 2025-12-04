from fastapi import APIRouter
from app.api.v1 import daraz

api_router_daraz = APIRouter()

# Include all Daraz endpoints
api_router_daraz.include_router(daraz.router, prefix="/daraz", tags=["daraz"])
