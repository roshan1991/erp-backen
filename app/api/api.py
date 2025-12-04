from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os
from app.api.v1 import login, hr, supply_chain, crm, finance, manufacturing, pos, products, coupons, loyalty, users, sync

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(products.router, tags=["products"])
api_router.include_router(coupons.router, tags=["coupons"])
api_router.include_router(loyalty.router, tags=["loyalty"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])
api_router.include_router(hr.router, prefix="/hr", tags=["hr"])
api_router.include_router(supply_chain.router, prefix="/supply-chain", tags=["supply-chain"])
api_router.include_router(crm.router, prefix="/crm", tags=["crm"])
api_router.include_router(finance.router, prefix="/finance", tags=["finance"])
api_router.include_router(manufacturing.router, prefix="/manufacturing", tags=["manufacturing"])
api_router.include_router(pos.router, prefix="/pos", tags=["pos"])

# Image Upload Endpoint
@api_router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Create static directory if not exists
        os.makedirs("app/static/images", exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"app/static/images/{unique_filename}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"url": f"/static/images/{unique_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
