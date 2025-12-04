from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.manufacturing import BillOfMaterials, BOMComponent, WorkOrder
from app.schemas.manufacturing import BillOfMaterialsCreate, WorkOrderCreate

# BOM CRUD
def create_bom(db: Session, bom: BillOfMaterialsCreate) -> BillOfMaterials:
    db_bom = BillOfMaterials(
        product_id=bom.product_id,
        name=bom.name,
        version=bom.version,
        is_active=bom.is_active
    )
    db.add(db_bom)
    db.commit()
    db.refresh(db_bom)

    for component in bom.components:
        db_component = BOMComponent(
            bom_id=db_bom.id,
            component_product_id=component.component_product_id,
            quantity=component.quantity
        )
        db.add(db_component)
    
    db.commit()
    db.refresh(db_bom)
    return db_bom

def get_boms(db: Session, skip: int = 0, limit: int = 100) -> List[BillOfMaterials]:
    return db.query(BillOfMaterials).offset(skip).limit(limit).all()

# Work Order CRUD
def create_work_order(db: Session, work_order: WorkOrderCreate) -> WorkOrder:
    db_work_order = WorkOrder(
        product_id=work_order.product_id,
        quantity=work_order.quantity,
        status=work_order.status,
        start_date=work_order.start_date,
        end_date=work_order.end_date
    )
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order

def get_work_orders(db: Session, skip: int = 0, limit: int = 100) -> List[WorkOrder]:
    return db.query(WorkOrder).offset(skip).limit(limit).all()
