from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Supplier(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    contact_person = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    products = relationship("InventoryProduct", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

class InventoryProduct(Base):
    __tablename__ = "inventory_products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, default=0)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=True)
    
    supplier = relationship("Supplier", back_populates="products")
    order_items = relationship("PurchaseOrderItem", back_populates="product")

class PurchaseOrder(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="PENDING") # PENDING, RECEIVED, CANCELLED
    supplier_id = Column(Integer, ForeignKey("supplier.id"))
    total_amount = Column(Float, default=0.0)
    
    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="order")

class PurchaseOrderItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchaseorder.id"))
    product_id = Column(Integer, ForeignKey("inventory_products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("InventoryProduct", back_populates="order_items")
