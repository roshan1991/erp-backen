from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.manufacturing import BillOfMaterials, BillOfMaterialsCreate, WorkOrder, WorkOrderCreate
from app.crud import crud_manufacturing

router = APIRouter()

# BOMs
@router.post("/boms", response_model=BillOfMaterials)
def create_bom(
    bom: BillOfMaterialsCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_manufacturing.create_bom(db=db, bom=bom)

@router.get("/boms", response_model=List[BillOfMaterials])
def read_boms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_manufacturing.get_boms(db, skip=skip, limit=limit)

# Work Orders
@router.post("/work-orders", response_model=WorkOrder)
def create_work_order(
    work_order: WorkOrderCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_manufacturing.create_work_order(db=db, work_order=work_order)

@router.get("/work-orders", response_model=List[WorkOrder])
def read_work_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_manufacturing.get_work_orders(db, skip=skip, limit=limit)
