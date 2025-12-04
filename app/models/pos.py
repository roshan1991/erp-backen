from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class SessionStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

class PaymentMethod(str, enum.Enum):
    CASH = "CASH"
    CARD = "CARD"
    TRANSFER = "TRANSFER"

class POSSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default=SessionStatus.OPEN)
    opening_cash = Column(Float, default=0.0)
    closing_cash = Column(Float, nullable=True)
    
    user = relationship("User")
    orders = relationship("POSOrder", back_populates="session")

class POSOrder(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("possession.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=True)
    total_amount = Column(Float, default=0.0)
    status = Column(String, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("POSSession", back_populates="orders")
    customer = relationship("Customer")
    items = relationship("POSOrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")

class POSOrderItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("posorder.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    order = relationship("POSOrder", back_populates="items")
    product = relationship("Product")

class Payment(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("posorder.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String, default=PaymentMethod.CASH)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("POSOrder", back_populates="payments")
