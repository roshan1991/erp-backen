from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class WorkOrderStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# BOM Component Schemas
class BOMComponentBase(BaseModel):
    component_product_id: int
    quantity: float

class BOMComponentCreate(BOMComponentBase):
    pass

class BOMComponent(BOMComponentBase):
    id: int
    bom_id: int

    class Config:
        from_attributes = True

# BOM Schemas
class BillOfMaterialsBase(BaseModel):
    product_id: int
    name: str
    version: str = "1.0"
    is_active: bool = True

class BillOfMaterialsCreate(BillOfMaterialsBase):
    components: List[BOMComponentCreate]

class BillOfMaterials(BillOfMaterialsBase):
    id: int
    components: List[BOMComponent] = []

    class Config:
        from_attributes = True

# Work Order Schemas
class WorkOrderBase(BaseModel):
    product_id: int
    quantity: float
    status: WorkOrderStatus = WorkOrderStatus.PLANNED
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class WorkOrderCreate(WorkOrderBase):
    pass

class WorkOrder(WorkOrderBase):
    id: int

    class Config:
        from_attributes = True
