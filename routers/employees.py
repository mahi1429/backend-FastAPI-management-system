from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from models.department import Department
from models.employee import Employee
from schemas.employee import RegisterEmployee, EmployeeResponse, UpdateEmployee
from security.utils import require_hr


router = APIRouter(
    prefix= "/employees",
    tags = ['Employees']
)

@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=201,
    dependencies=[Depends(require_hr)],
)
def add_employee(employee: RegisterEmployee, db: Session = Depends(get_db)):
    if employee.department_id is not None:
        department = db.query(Department).filter(Department.id == employee.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        birth_date=employee.birth_date,
        department_id=employee.department_id,
    )
    emp = db.query(Employee).filter(Employee.email == new_employee.email).first()
    if emp: 
        raise HTTPException(status_code=400, detail="Email already exists")

    db.add(new_employee)
    try:
        db.commit()
        db.refresh(new_employee)
    except:
        db.rollback()
        raise
    return new_employee

@router.get("/", response_model=List[EmployeeResponse], dependencies=[Depends(require_hr)])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(require_hr)],
)
def update_employee(employee_id: int, employee: UpdateEmployee, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    if employee.department_id is not None:
        department = db.query(Department).filter(Department.id == employee.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    for field, value in employee.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)

    try:
        db.commit()
        db.refresh(emp)
    except Exception:
        db.rollback()
        raise 

    return emp

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(require_hr)],
)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp