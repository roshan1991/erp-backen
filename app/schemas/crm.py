from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class LeadStage(str, Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    PROPOSAL = "PROPOSAL"
    WON = "WON"
    LOST = "LOST"

class InteractionType(str, Enum):
    CALL = "CALL"
    EMAIL = "EMAIL"
    MEETING = "MEETING"
    NOTE = "NOTE"

# Interaction Schemas
class InteractionBase(BaseModel):
    type: InteractionType
    notes: Optional[str] = None
    date: datetime = datetime.utcnow()
    customer_id: int

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int

    class Config:
        from_attributes = True

# Lead Schemas
class LeadBase(BaseModel):
    title: str
    description: Optional[str] = None
    value: float = 0.0
    stage: LeadStage = LeadStage.NEW
    customer_id: Optional[int] = None

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: str = "ACTIVE"

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    leads: List[Lead] = []
    interactions: List[Interaction] = []

    class Config:
        from_attributes = True
