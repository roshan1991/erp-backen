from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class AccountType(str, Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"

# Account Schemas
class AccountBase(BaseModel):
    code: str
    name: str
    type: AccountType
    description: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[AccountType] = None

class Account(AccountBase):
    id: int
    balance: float

    class Config:
        from_attributes = True

# Journal Entry Schemas
class JournalEntryLineBase(BaseModel):
    account_id: int
    debit: float = 0.0
    credit: float = 0.0
    description: Optional[str] = None

class JournalEntryLineCreate(JournalEntryLineBase):
    pass

class JournalEntryLine(JournalEntryLineBase):
    id: int
    journal_entry_id: int

    class Config:
        from_attributes = True

class JournalEntryBase(BaseModel):
    date: datetime
    description: str
    reference: Optional[str] = None
    status: Optional[str] = "DRAFT"

class JournalEntryCreate(JournalEntryBase):
    lines: List[JournalEntryLineCreate]

class JournalEntry(JournalEntryBase):
    id: int
    lines: List[JournalEntryLine]

    class Config:
        from_attributes = True

# AP Invoice Schemas
class APInvoiceBase(BaseModel):
    invoice_number: str
    supplier_id: int
    date: datetime
    due_date: Optional[datetime] = None
    total_amount: float
    status: Optional[str] = "DRAFT"

class APInvoiceCreate(APInvoiceBase):
    pass

class APInvoice(APInvoiceBase):
    id: int

    class Config:
        from_attributes = True

# AR Invoice Schemas
class ARInvoiceBase(BaseModel):
    invoice_number: str
    customer_id: int
    date: datetime
    due_date: Optional[datetime] = None
    total_amount: float
    status: Optional[str] = "DRAFT"

class ARInvoiceCreate(ARInvoiceBase):
    pass

class ARInvoice(ARInvoiceBase):
    id: int

    class Config:
        from_attributes = True

# Bank Statement Schemas
class BankStatementBase(BaseModel):
    bank_account_id: int
    date: datetime
    reference: Optional[str] = None
    description: Optional[str] = None
    amount: float
    reconciled: bool = False

class BankStatementCreate(BankStatementBase):
    pass

class BankStatement(BankStatementBase):
    id: int

    class Config:
        from_attributes = True
