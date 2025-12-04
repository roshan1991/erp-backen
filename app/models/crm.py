from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class LeadStage(str, enum.Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    PROPOSAL = "PROPOSAL"
    WON = "WON"
    LOST = "LOST"

class InteractionType(str, enum.Enum):
    CALL = "CALL"
    EMAIL = "EMAIL"
    MEETING = "MEETING"
    NOTE = "NOTE"

class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    status = Column(String, default="ACTIVE") # ACTIVE, INACTIVE
    
    leads = relationship("Lead", back_populates="customer")
    interactions = relationship("Interaction", back_populates="customer")

class Lead(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    value = Column(Float, default=0.0)
    stage = Column(String, default=LeadStage.NEW)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="leads")

class Interaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, default=InteractionType.NOTE)
    notes = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    
    customer = relationship("Customer", back_populates="interactions")
