from sqlalchemy import Column, Integer, Float, Boolean
from app.db.base import Base


class LoyaltySettings(Base):
    __tablename__ = "loyalty_settings"

    id = Column(Integer, primary_key=True, index=True)
    points_per_dollar = Column(Float, default=1.0)  # Points earned per dollar spent
    redemption_rate = Column(Float, default=0.01)  # Dollar value per point
    is_enabled = Column(Boolean, default=True)
