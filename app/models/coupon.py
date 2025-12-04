from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.db.base import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(String(20), nullable=False)  # percentage or fixed
    value = Column(Float, nullable=False)
    min_purchase = Column(Float, default=0)
    expiry_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
