from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.crm import Customer, Lead, Interaction
from app.schemas.crm import CustomerCreate, LeadCreate, InteractionCreate

# Customer CRUD
def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        company=customer.company,
        status=customer.status
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()

# Lead CRUD
def create_lead(db: Session, lead: LeadCreate) -> Lead:
    db_lead = Lead(
        title=lead.title,
        description=lead.description,
        value=lead.value,
        stage=lead.stage,
        customer_id=lead.customer_id
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_leads(db: Session, skip: int = 0, limit: int = 100) -> List[Lead]:
    return db.query(Lead).offset(skip).limit(limit).all()

# Interaction CRUD
def create_interaction(db: Session, interaction: InteractionCreate) -> Interaction:
    db_interaction = Interaction(
        type=interaction.type,
        notes=interaction.notes,
        date=interaction.date,
        customer_id=interaction.customer_id
    )
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

def get_interactions(db: Session, skip: int = 0, limit: int = 100) -> List[Interaction]:
    return db.query(Interaction).offset(skip).limit(limit).all()
