from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api import deps
from app.models.product import Product
from pydantic import BaseModel
import uuid
import os

router = APIRouter()


# Pydantic schemas
class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    stock: int = 0
    barcode: Optional[str] = None
    image: Optional[str] = None
    status: str = "In Stock"


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    barcode: Optional[str] = None
    image: Optional[str] = None
    status: Optional[str] = None


@router.get("/products")
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of products with pagination and search"""
    query = db.query(Product)
    
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.barcode.ilike(f"%{search}%"))
        )
    
    if category:
        query = query.filter(Product.category == category)
    
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "products": products
    }


@router.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Get single product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products")
def create_product(
    product: ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Create a new product"""
    # Check if barcode already exists
    if product.barcode:
        existing = db.query(Product).filter(Product.barcode == product.barcode).first()
        if existing:
            raise HTTPException(status_code=400, detail="Barcode already exists")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Update a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check barcode uniqueness if updating
    if product.barcode and product.barcode != db_product.barcode:
        existing = db.query(Product).filter(Product.barcode == product.barcode).first()
        if existing:
            raise HTTPException(status_code=400, detail="Barcode already exists")
    
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Delete a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
