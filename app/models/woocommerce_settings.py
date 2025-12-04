from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class WooCommerceSettings(Base):
    __tablename__ = "woocommerce_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    store_url = Column(String, nullable=False)
    consumer_key = Column(String, nullable=False)
    consumer_secret = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
