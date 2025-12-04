import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.finance import Account, JournalEntry, APInvoice, ARInvoice, BankStatement, AccountType
from app.schemas.finance import AccountCreate, JournalEntryCreate, JournalEntryLineCreate, APInvoiceCreate, ARInvoiceCreate, BankStatementCreate
from app.crud import crud_finance
from datetime import datetime

# Setup in-memory SQLite db for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def test_finance_crud():
    db = TestingSessionLocal()
    
    # 1. Create Account
    account_in = AccountCreate(code="1001", name="Cash", type=AccountType.ASSET, description="Main Cash Account")
    account = crud_finance.create_account(db, account_in)
    print(f"Created Account: {account.name} (ID: {account.id})")
    
    # 2. Create Journal Entry
    line1 = JournalEntryLineCreate(account_id=account.id, debit=100.0, credit=0.0, description="Initial Deposit")
    entry_in = JournalEntryCreate(
        date=datetime.utcnow(),
        description="Opening Balance",
        reference="REF001",
        status="POSTED",
        lines=[line1]
    )
    entry = crud_finance.create_journal_entry(db, entry_in)
    print(f"Created Journal Entry: {entry.description} (ID: {entry.id})")
    
    # Verify Balance Update
    db.refresh(account)
    print(f"Account Balance: {account.balance}")
    assert account.balance == 100.0
    
    # 3. Create AP Invoice
    ap_in = APInvoiceCreate(
        invoice_number="INV-SUP-001",
        supplier_id=1, # Mock ID
        date=datetime.utcnow(),
        total_amount=500.0,
        status="DRAFT"
    )
    ap_invoice = crud_finance.create_ap_invoice(db, ap_in)
    print(f"Created AP Invoice: {ap_invoice.invoice_number} (ID: {ap_invoice.id})")
    
    # 4. Create AR Invoice
    ar_in = ARInvoiceCreate(
        invoice_number="INV-CUS-001",
        customer_id=1, # Mock ID
        date=datetime.utcnow(),
        total_amount=1200.0,
        status="DRAFT"
    )
    ar_invoice = crud_finance.create_ar_invoice(db, ar_in)
    print(f"Created AR Invoice: {ar_invoice.invoice_number} (ID: {ar_invoice.id})")
    
    # 5. Create Bank Statement
    bs_in = BankStatementCreate(
        bank_account_id=account.id,
        date=datetime.utcnow(),
        amount=100.0,
        description="Deposit",
        reconciled=False
    )
    statement = crud_finance.create_bank_statement(db, bs_in)
    print(f"Created Bank Statement: {statement.amount} (ID: {statement.id})")
    
    print("All tests passed!")
    db.close()

if __name__ == "__main__":
    test_finance_crud()
