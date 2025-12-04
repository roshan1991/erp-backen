from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.pos import POSSession, POSSessionCreate, POSSessionUpdate, POSOrder, POSOrderCreate
from app.crud import crud_pos

router = APIRouter()

# Sessions
@router.post("/sessions", response_model=POSSession)
def create_session(
    session: POSSessionCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    active_session = crud_pos.get_active_session(db, user_id=current_user.id)
    if active_session:
        raise HTTPException(status_code=400, detail="User already has an active session")
    return crud_pos.create_session(db=db, session=session, user_id=current_user.id)

@router.put("/sessions/{session_id}/close", response_model=POSSession)
def close_session(
    session_id: int,
    session_update: POSSessionUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    session = crud_pos.close_session(db=db, session_id=session_id, session_update=session_update)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/sessions/active", response_model=POSSession)
def get_active_session(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    session = crud_pos.get_active_session(db, user_id=current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="No active session found")
    return session

# Orders
@router.post("/orders", response_model=POSOrder)
def create_order(
    order: POSOrderCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_pos.create_order(db=db, order=order)

@router.get("/orders", response_model=List[POSOrder])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_pos.get_orders(db, skip=skip, limit=limit)

@router.get("/orders/{order_id}", response_model=POSOrder)
def read_order(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    order = crud_pos.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
