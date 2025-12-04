from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Department(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    job_title = Column(String, nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=True)
    
    department = relationship("Department", back_populates="employees")
    payrolls = relationship("Payroll", back_populates="employee")

class Payroll(Base):
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    pay_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="PROCESSED") # PROCESSED, PENDING
    
    employee = relationship("Employee", back_populates="payrolls")
