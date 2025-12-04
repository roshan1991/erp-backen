from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.supply_chain import Supplier, InventoryProduct, PurchaseOrder, PurchaseOrderItem
from app.schemas.supply_chain import SupplierCreate, ProductCreate, PurchaseOrderCreate

# Supplier CRUD
def create_supplier(db: Session, supplier: SupplierCreate) -> Supplier:
    db_supplier = Supplier(
        name=supplier.name,
        contact_person=supplier.contact_person,
        email=supplier.email,
        phone=supplier.phone,
        address=supplier.address
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_suppliers(db: Session, skip: int = 0, limit: int = 100) -> List[Supplier]:
    return db.query(Supplier).offset(skip).limit(limit).all()

# Product CRUD
def create_product(db: Session, product: ProductCreate) -> InventoryProduct:
    db_product = InventoryProduct(
        sku=product.sku,
        name=product.name,
        description=product.description,
        price=product.price,
        cost_price=product.cost_price,
        quantity_in_stock=product.quantity_in_stock,
        supplier_id=product.supplier_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[InventoryProduct]:
    return db.query(InventoryProduct).offset(skip).limit(limit).all()

# Purchase Order CRUD
def create_purchase_order(db: Session, order: PurchaseOrderCreate) -> PurchaseOrder:
    # Calculate total amount
    total_amount = sum(item.quantity * item.unit_price for item in order.items)
    
    db_order = PurchaseOrder(
        supplier_id=order.supplier_id,
        status=order.status,
        total_amount=total_amount
    )
    db.add(db_order)
    db.flush()

    for item in order.items:
        db_item = PurchaseOrderItem(
            purchase_order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(db_item)
        
        # Update product stock if order is received (simplified logic)
        # In a real system, this would happen on a separate "Receive" action
        if order.status == "RECEIVED":
            product = db.query(InventoryProduct).filter(InventoryProduct.id == item.product_id).first()
            if product:
                product.quantity_in_stock += item.quantity

    db.commit()
    db.refresh(db_order)
    return db_order

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100) -> List[PurchaseOrder]:
    return db.query(PurchaseOrder).offset(skip).limit(limit).all()
