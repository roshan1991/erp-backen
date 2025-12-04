from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float
    cost_price: float
    quantity_in_stock: int = 0
    supplier_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# Purchase Order Schemas
class PurchaseOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    purchase_order_id: int

    class Config:
        from_attributes = True

class PurchaseOrderBase(BaseModel):
    supplier_id: int
    status: str = "PENDING"

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]

class PurchaseOrder(PurchaseOrderBase):
    id: int
    date: datetime
    total_amount: float
    items: List[PurchaseOrderItem]

    class Config:
        from_attributes = True
