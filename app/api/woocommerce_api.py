from fastapi import APIRouter
from app.api.v1 import woocommerce

api_router_woocommerce = APIRouter()

# Include all WooCommerce endpoints
api_router_woocommerce.include_router(woocommerce.router, prefix="/woocommerce", tags=["woocommerce"])
