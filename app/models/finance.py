from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class AccountType(str, enum.Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"

class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) # Storing Enum as String for simplicity in SQLite/Postgres compatibility if needed, but here we use String
    description = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    
    transaction_lines = relationship("JournalEntryLine", back_populates="account")

class JournalEntryStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    POSTED = "POSTED"

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=False)
    reference = Column(String, nullable=True)
    status = Column(String, default=JournalEntryStatus.DRAFT)
    
    lines = relationship("JournalEntryLine", back_populates="journal_entry", cascade="all, delete-orphan")

class JournalEntryLine(Base):
    __tablename__ = "journal_entry_lines"

    id = Column(Integer, primary_key=True, index=True)
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id"))
    account_id = Column(Integer, ForeignKey("account.id"))
    debit = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    description = Column(String, nullable=True)
    
    journal_entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="transaction_lines")

class APInvoice(Base):
    __tablename__ = "ap_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier.id"))
    date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="DRAFT") # DRAFT, POSTED, PAID
    
    # supplier = relationship("Supplier") # Assuming Supplier is in another module, might need import or string reference if not in same Base
    # For now, we rely on foreign key. If we need relationship, we need to import Supplier or use string if registered.
    # Given Supplier is in supply_chain.py, we might need to ensure Base is shared or use string "Supplier" if they share Base.
    # They share app.db.base.Base, so string reference works if loaded.

class ARInvoice(Base):
    __tablename__ = "ar_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="DRAFT") # DRAFT, POSTED, PAID

class BankStatement(Base):
    __tablename__ = "bank_statements"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_id = Column(Integer, ForeignKey("account.id")) # Link to GL Account for Bank
    date = Column(DateTime, default=datetime.utcnow)
    reference = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False) # Positive for deposit, Negative for withdrawal
    reconciled = Column(Boolean, default=False)
