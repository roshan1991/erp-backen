from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

from app.api.api import api_router
from app.api.daraz_api import api_router_daraz
from app.api.social_media_api import api_router_social_media
from app.api.woocommerce_api import api_router_woocommerce
from app.api.v1.woocommerce_test import router as woocommerce_test_router

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router_daraz, prefix=settings.API_V1_STR)
app.include_router(api_router_social_media, prefix=settings.API_V1_STR)
app.include_router(api_router_woocommerce, prefix=settings.API_V1_STR)
app.include_router(woocommerce_test_router, prefix=f"{settings.API_V1_STR}/woocommerce-test", tags=["woocommerce-test"])

@app.get("/")
def root():
    return {"message": "Welcome to ERP System API"}
