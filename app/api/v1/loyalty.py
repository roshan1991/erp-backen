from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.loyalty_settings import LoyaltySettings
from pydantic import BaseModel

router = APIRouter()


# Pydantic schema
class LoyaltySettingsUpdate(BaseModel):
    points_per_dollar: float
    redemption_rate: float
    is_enabled: bool


@router.get("/loyalty/settings")
def get_loyalty_settings(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Get loyalty settings"""
    settings = db.query(LoyaltySettings).first()
    
    # Create default settings if none exist
    if not settings:
        settings = LoyaltySettings(
            points_per_dollar=1.0,
            redemption_rate=0.01,
            is_enabled=True
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings


@router.put("/loyalty/settings")
def update_loyalty_settings(
    settings: LoyaltySettingsUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Update loyalty settings"""
    db_settings = db.query(LoyaltySettings).first()
    
    if not db_settings:
        # Create if doesn't exist
        db_settings = LoyaltySettings(**settings.dict())
        db.add(db_settings)
    else:
        # Update existing
        for field, value in settings.dict().items():
            setattr(db_settings, field, value)
    
    db.commit()
    db.refresh(db_settings)
    return db_settings
