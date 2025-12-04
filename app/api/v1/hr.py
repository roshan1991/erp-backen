from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.hr import Department, DepartmentCreate, Employee, EmployeeCreate, Payroll, PayrollCreate
from app.crud import crud_hr

router = APIRouter()

# Departments
@router.post("/departments", response_model=Department)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_hr.create_department(db=db, department=department)

@router.get("/departments", response_model=List[Department])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_hr.get_departments(db, skip=skip, limit=limit)

# Employees
@router.post("/employees", response_model=Employee)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_hr.create_employee(db=db, employee=employee)

@router.get("/employees", response_model=List[Employee])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_hr.get_employees(db, skip=skip, limit=limit)

# Payroll
@router.post("/payroll", response_model=Payroll)
def create_payroll(
    payroll: PayrollCreate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_hr.create_payroll(db=db, payroll=payroll)

@router.get("/payroll", response_model=List[Payroll])
def read_payrolls(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    return crud_hr.get_payrolls(db, skip=skip, limit=limit)
