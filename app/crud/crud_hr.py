from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.hr import Department, Employee, Payroll
from app.schemas.hr import DepartmentCreate, EmployeeCreate, PayrollCreate

# Department CRUD
def create_department(db: Session, department: DepartmentCreate) -> Department:
    db_department = Department(
        name=department.name,
        description=department.description
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_departments(db: Session, skip: int = 0, limit: int = 100) -> List[Department]:
    return db.query(Department).offset(skip).limit(limit).all()

# Employee CRUD
def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        phone=employee.phone,
        job_title=employee.job_title,
        hire_date=employee.hire_date,
        salary=employee.salary,
        department_id=employee.department_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()

# Payroll CRUD
def create_payroll(db: Session, payroll: PayrollCreate) -> Payroll:
    db_payroll = Payroll(
        employee_id=payroll.employee_id,
        pay_date=payroll.pay_date,
        amount=payroll.amount,
        status=payroll.status
    )
    db.add(db_payroll)
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def get_payrolls(db: Session, skip: int = 0, limit: int = 100) -> List[Payroll]:
    return db.query(Payroll).offset(skip).limit(limit).all()
