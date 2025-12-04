from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.crm import Customer, CustomerCreate, Lead, LeadCreate, Interaction, InteractionCreate
from app.crud import crud_crm

router = APIRouter()

# Customers
@router.post("/customers", response_model=Customer)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_crm.create_customer(db=db, customer=customer)

@router.get("/customers", response_model=List[Customer])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_crm.get_customers(db, skip=skip, limit=limit)

# Leads
@router.post("/leads", response_model=Lead)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_crm.create_lead(db=db, lead=lead)

@router.get("/leads", response_model=List[Lead])
def read_leads(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_crm.get_leads(db, skip=skip, limit=limit)

# Interactions
@router.post("/interactions", response_model=Interaction)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_crm.create_interaction(db=db, interaction=interaction)

@router.get("/interactions", response_model=List[Interaction])
def read_interactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_crm.get_interactions(db, skip=skip, limit=limit)
