from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database.db import get_db
from models.department import Department
from models.user import User
from schemas.department import CreateDepartment, DepartmentDetailResponse,DepartmentResponse
from security.utils import require_hr, require_roles
from models.user import UserRole


router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=201,
    dependencies=[Depends(require_hr)],
)
def create_department(department: CreateDepartment, db: Session = Depends(get_db)):
    new_department = Department(name=department.name)
    db.add(new_department)
    try:
        db.commit()
        db.refresh(new_department)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Department name already exists") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while creating department") from exc

    return new_department


@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.HR, UserRole.MAINTENANCE_MANAGER)),
):
    
    query = db.query(Department)
    if current_user.role == UserRole.MAINTENANCE_MANAGER.value:
        if current_user.department_id is None:
            raise HTTPException(status_code=403, detail="Manager account has no department")
        query = query.filter(Department.id == current_user.department_id)
    return query.all()


@router.get("/{department_id}", response_model=DepartmentDetailResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.MAINTENANCE_MANAGER)),
):
    
    if current_user.department_id != department_id:
        raise HTTPException(status_code=403, detail="Managers may only view their own department")
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department