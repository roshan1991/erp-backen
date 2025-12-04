from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.finance import Account, AccountCreate, JournalEntry, JournalEntryCreate, APInvoice, APInvoiceCreate, ARInvoice, ARInvoiceCreate, BankStatement, BankStatementCreate
from app.crud import crud_finance

router = APIRouter()

@router.post("/accounts", response_model=Account)
def create_account(
    account: AccountCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.create_account(db=db, account=account)

@router.get("/accounts", response_model=List[Account])
def read_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.get_accounts(db, skip=skip, limit=limit)

@router.post("/journal-entries", response_model=JournalEntry)
def create_journal_entry(
    journal_entry: JournalEntryCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.create_journal_entry(db=db, journal_entry=journal_entry)

@router.get("/journal-entries", response_model=List[JournalEntry])
def read_journal_entries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.get_journal_entries(db, skip=skip, limit=limit)

@router.post("/ap-invoices", response_model=APInvoice)
def create_ap_invoice(
    invoice: APInvoiceCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.create_ap_invoice(db=db, invoice=invoice)

@router.get("/ap-invoices", response_model=List[APInvoice])
def read_ap_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.get_ap_invoices(db, skip=skip, limit=limit)

@router.post("/ar-invoices", response_model=ARInvoice)
def create_ar_invoice(
    invoice: ARInvoiceCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.create_ar_invoice(db=db, invoice=invoice)

@router.get("/ar-invoices", response_model=List[ARInvoice])
def read_ar_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.get_ar_invoices(db, skip=skip, limit=limit)

@router.post("/bank-statements", response_model=BankStatement)
def create_bank_statement(
    statement: BankStatementCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.create_bank_statement(db=db, statement=statement)

@router.get("/bank-statements", response_model=List[BankStatement])
def read_bank_statements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_finance.get_bank_statements(db, skip=skip, limit=limit)
