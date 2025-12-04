from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import date

# Department Schemas
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True

# Employee Schemas
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    job_title: str
    hire_date: date
    salary: float
    department_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

# Payroll Schemas
class PayrollBase(BaseModel):
    employee_id: int
    pay_date: date
    amount: float
    status: str = "PROCESSED"

class PayrollCreate(PayrollBase):
    pass

class Payroll(PayrollBase):
    id: int

    class Config:
        from_attributes = True
