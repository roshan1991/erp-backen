from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SessionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class PaymentMethod(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    TRANSFER = "TRANSFER"

# Payment Schemas
class PaymentBase(BaseModel):
    amount: float
    method: PaymentMethod

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Order Item Schemas
class POSOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class POSOrderItemCreate(POSOrderItemBase):
    pass

class POSOrderItem(POSOrderItemBase):
    id: int
    subtotal: float

    class Config:
        from_attributes = True

# Order Schemas
class POSOrderBase(BaseModel):
    customer_id: Optional[int] = None
    total_amount: float
    status: str = "COMPLETED"

class POSOrderCreate(POSOrderBase):
    session_id: int
    items: List[POSOrderItemCreate]
    payments: List[PaymentCreate]

class POSOrder(POSOrderBase):
    id: int
    created_at: datetime
    items: List[POSOrderItem] = []
    payments: List[Payment] = []

    class Config:
        from_attributes = True

# Session Schemas
class POSSessionBase(BaseModel):
    opening_cash: float = 0.0

class POSSessionCreate(POSSessionBase):
    pass

class POSSessionUpdate(BaseModel):
    closing_cash: float
    status: SessionStatus = SessionStatus.CLOSED
    end_time: datetime = datetime.utcnow()

class POSSession(POSSessionBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: SessionStatus
    closing_cash: Optional[float] = None

    class Config:
        from_attributes = True
