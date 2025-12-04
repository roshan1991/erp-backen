from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.pos import POSSession, POSOrder, POSOrderItem, Payment, SessionStatus
from app.schemas.pos import POSSessionCreate, POSSessionUpdate, POSOrderCreate

# Session CRUD
def create_session(db: Session, session: POSSessionCreate, user_id: int) -> POSSession:
    db_session = POSSession(
        user_id=user_id,
        opening_cash=session.opening_cash,
        status=SessionStatus.OPEN
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session(db: Session, session_id: int) -> Optional[POSSession]:
    return db.query(POSSession).filter(POSSession.id == session_id).first()

def get_active_session(db: Session, user_id: int) -> Optional[POSSession]:
    return db.query(POSSession).filter(
        POSSession.user_id == user_id,
        POSSession.status == SessionStatus.OPEN
    ).first()

def close_session(db: Session, session_id: int, session_update: POSSessionUpdate) -> POSSession:
    db_session = get_session(db, session_id)
    if not db_session:
        return None
    
    db_session.closing_cash = session_update.closing_cash
    db_session.status = session_update.status
    db_session.end_time = session_update.end_time
    
    db.commit()
    db.refresh(db_session)
    return db_session

# Order CRUD
def create_order(db: Session, order: POSOrderCreate) -> POSOrder:
    db_order = POSOrder(
        session_id=order.session_id,
        customer_id=order.customer_id,
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add items
    for item in order.items:
        db_item = POSOrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price
        )
        db.add(db_item)
    
    # Add payments
    for payment in order.payments:
        db_payment = Payment(
            order_id=db_order.id,
            amount=payment.amount,
            method=payment.method
        )
        db.add(db_payment)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[POSOrder]:
    return db.query(POSOrder).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int) -> Optional[POSOrder]:
    return db.query(POSOrder).filter(POSOrder.id == order_id).first()
