from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api import deps
from app.models.coupon import Coupon
from pydantic import BaseModel
from datetime import date

router = APIRouter()


# Pydantic schemas
class CouponCreate(BaseModel):
    code: str
    type: str  # percentage or fixed
    value: float
    min_purchase: float = 0
    expiry_date: Optional[date] = None
    is_active: bool = True


class CouponUpdate(BaseModel):
    code: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = None
    min_purchase: Optional[float] = None
    expiry_date: Optional[date] = None
    is_active: Optional[bool] = None


@router.get("/coupons")
def get_coupons(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of coupons"""
    total = db.query(Coupon).count()
    coupons = db.query(Coupon).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "coupons": coupons
    }


@router.get("/coupons/{coupon_id}")
def get_coupon(
    coupon_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Get single coupon by ID"""
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon


@router.post("/coupons")
def create_coupon(
    coupon: CouponCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Create a new coupon"""
    # Check if code already exists
    existing = db.query(Coupon).filter(Coupon.code == coupon.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Coupon code already exists")
    
    db_coupon = Coupon(**coupon.dict())
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon


@router.put("/coupons/{coupon_id}")
def update_coupon(
    coupon_id: int,
    coupon: CouponUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Update a coupon"""
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    # Check code uniqueness if updating
    if coupon.code and coupon.code != db_coupon.code:
        existing = db.query(Coupon).filter(Coupon.code == coupon.code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Coupon code already exists")
    
    update_data = coupon.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_coupon, field, value)
    
    db.commit()
    db.refresh(db_coupon)
    return db_coupon


@router.delete("/coupons/{coupon_id}")
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Delete a coupon"""
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    db.delete(db_coupon)
    db.commit()
    return {"message": "Coupon deleted successfully"}


@router.post("/coupons/validate")
def validate_coupon(
    code: str,
    purchase_amount: float,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Validate a coupon code"""
    coupon = db.query(Coupon).filter(Coupon.code == code, Coupon.is_active == True).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon code")
    
    # Check expiry
    if coupon.expiry_date and coupon.expiry_date < date.today():
        raise HTTPException(status_code=400, detail="Coupon has expired")
    
    # Check minimum purchase
    if purchase_amount < coupon.min_purchase:
        raise HTTPException(
            status_code=400, 
            detail=f"Minimum purchase of ${coupon.min_purchase} required"
        )
    
    return {
        "valid": True,
        "coupon": coupon
    }
