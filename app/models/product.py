from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    barcode = Column(String(100), unique=True, index=True)
    image = Column(String(500))  # URL or path to image
    status = Column(String(50), default="In Stock")  # In Stock, Out of Stock, Low Stock
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
