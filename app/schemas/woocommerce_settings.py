from pydantic import BaseModel
from typing import Optional


class WooCommerceSettingsBase(BaseModel):
    store_url: str
    consumer_key: str
    consumer_secret: str
    is_active: bool = True


class WooCommerceSettingsCreate(WooCommerceSettingsBase):
    pass


class WooCommerceSettingsUpdate(BaseModel):
    store_url: Optional[str] = None
    consumer_key: Optional[str] = None
    consumer_secret: Optional[str] = None
    is_active: Optional[bool] = None


class WooCommerceSettings(WooCommerceSettingsBase):
    id: int
    
    class Config:
        from_attributes = True
