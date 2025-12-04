from sqlalchemy.orm import Session
from typing import Optional
from app.models.woocommerce_settings import WooCommerceSettings
from app.schemas.woocommerce_settings import WooCommerceSettingsCreate, WooCommerceSettingsUpdate


def get_settings(db: Session) -> Optional[WooCommerceSettings]:
    """Get the active WooCommerce settings (there should only be one)"""
    return db.query(WooCommerceSettings).filter(WooCommerceSettings.is_active == True).first()


def create_settings(db: Session, settings: WooCommerceSettingsCreate) -> WooCommerceSettings:
    """Create new WooCommerce settings"""
    # Deactivate any existing settings
    db.query(WooCommerceSettings).update({"is_active": False})
    
    db_settings = WooCommerceSettings(**settings.dict())
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings


def update_settings(db: Session, settings_id: int, settings: WooCommerceSettingsUpdate) -> Optional[WooCommerceSettings]:
    """Update existing WooCommerce settings"""
    db_settings = db.query(WooCommerceSettings).filter(WooCommerceSettings.id == settings_id).first()
    if not db_settings:
        return None
    
    update_data = settings.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_settings, key, value)
    
    db.commit()
    db.refresh(db_settings)
    return db_settings
