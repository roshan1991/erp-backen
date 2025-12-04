from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.supply_chain import Supplier, SupplierCreate, Product, ProductCreate, PurchaseOrder, PurchaseOrderCreate
from app.crud import crud_supply_chain

router = APIRouter()

# Suppliers
@router.post("/suppliers", response_model=Supplier)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_supply_chain.create_supplier(db=db, supplier=supplier)

@router.get("/suppliers", response_model=List[Supplier])
def read_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_supply_chain.get_suppliers(db, skip=skip, limit=limit)

# Products
@router.post("/products", response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_supply_chain.create_product(db=db, product=product)

@router.get("/products", response_model=List[Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_supply_chain.get_products(db, skip=skip, limit=limit)

# Purchase Orders
@router.post("/orders", response_model=PurchaseOrder)
def create_purchase_order(
    order: PurchaseOrderCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_supply_chain.create_purchase_order(db=db, order=order)

@router.get("/orders", response_model=List[PurchaseOrder])
def read_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_supply_chain.get_purchase_orders(db, skip=skip, limit=limit)
