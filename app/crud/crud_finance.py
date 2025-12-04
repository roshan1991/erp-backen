from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.finance import Account, JournalEntry, JournalEntryLine, APInvoice, ARInvoice, BankStatement
from app.schemas.finance import AccountCreate, AccountUpdate, JournalEntryCreate, APInvoiceCreate, ARInvoiceCreate, BankStatementCreate

# Account CRUD
def create_account(db: Session, account: AccountCreate) -> Account:
    db_account = Account(
        code=account.code,
        name=account.name,
        type=account.type,
        description=account.description
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account(db: Session, account_id: int) -> Optional[Account]:
    return db.query(Account).filter(Account.id == account_id).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[Account]:
    return db.query(Account).offset(skip).limit(limit).all()

# JournalEntry CRUD
def create_journal_entry(db: Session, journal_entry: JournalEntryCreate) -> JournalEntry:
    db_journal_entry = JournalEntry(
        date=journal_entry.date,
        description=journal_entry.description,
        reference=journal_entry.reference,
        status=journal_entry.status
    )
    db.add(db_journal_entry)
    db.flush()

    for line in journal_entry.lines:
        db_line = JournalEntryLine(
            journal_entry_id=db_journal_entry.id,
            account_id=line.account_id,
            debit=line.debit,
            credit=line.credit,
            description=line.description
        )
        db.add(db_line)
        
        # Update account balance if POSTED
        if journal_entry.status == "POSTED":
            account = db.query(Account).filter(Account.id == line.account_id).first()
            if account:
                account.balance += (line.debit - line.credit)

    db.commit()
    db.refresh(db_journal_entry)
    return db_journal_entry

def get_journal_entries(db: Session, skip: int = 0, limit: int = 100) -> List[JournalEntry]:
    return db.query(JournalEntry).offset(skip).limit(limit).all()

def get_journal_entry(db: Session, entry_id: int) -> Optional[JournalEntry]:
    return db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()

# AP Invoice CRUD
def create_ap_invoice(db: Session, invoice: APInvoiceCreate) -> APInvoice:
    db_invoice = APInvoice(
        invoice_number=invoice.invoice_number,
        supplier_id=invoice.supplier_id,
        date=invoice.date,
        due_date=invoice.due_date,
        total_amount=invoice.total_amount,
        status=invoice.status
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_ap_invoices(db: Session, skip: int = 0, limit: int = 100) -> List[APInvoice]:
    return db.query(APInvoice).offset(skip).limit(limit).all()

# AR Invoice CRUD
def create_ar_invoice(db: Session, invoice: ARInvoiceCreate) -> ARInvoice:
    db_invoice = ARInvoice(
        invoice_number=invoice.invoice_number,
        customer_id=invoice.customer_id,
        date=invoice.date,
        due_date=invoice.due_date,
        total_amount=invoice.total_amount,
        status=invoice.status
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_ar_invoices(db: Session, skip: int = 0, limit: int = 100) -> List[ARInvoice]:
    return db.query(ARInvoice).offset(skip).limit(limit).all()

# Bank Statement CRUD
def create_bank_statement(db: Session, statement: BankStatementCreate) -> BankStatement:
    db_statement = BankStatement(
        bank_account_id=statement.bank_account_id,
        date=statement.date,
        reference=statement.reference,
        description=statement.description,
        amount=statement.amount,
        reconciled=statement.reconciled
    )
    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)
    return db_statement

def get_bank_statements(db: Session, skip: int = 0, limit: int = 100) -> List[BankStatement]:
    return db.query(BankStatement).offset(skip).limit(limit).all()
