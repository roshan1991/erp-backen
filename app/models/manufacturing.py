from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class WorkOrderStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class BillOfMaterials(Base):
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False)
    version = Column(String, default="1.0")
    is_active = Column(Boolean, default=True) # type: ignore
    
    product = relationship("Product")
    components = relationship("BOMComponent", back_populates="bom")

class BOMComponent(Base):
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("billofmaterials.id"), nullable=False)
    component_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    
    bom = relationship("BillOfMaterials", back_populates="components")
    component_product = relationship("Product", foreign_keys=[component_product_id])

class WorkOrder(Base):
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    status = Column(String, default=WorkOrderStatus.PLANNED)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    product = relationship("Product")
