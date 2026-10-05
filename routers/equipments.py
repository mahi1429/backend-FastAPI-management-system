from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from database.db import get_db
from models.department import Department
from models.equipment import Equipment
from models.user import User, UserRole
from schemas.equipment import RegisterEquipment, UpdateEquipment, EquipmentResponse
from security.utils import require_equipment_read, require_maintenance_manager


router = APIRouter(
    prefix= "/equipments",
    tags = ['Equipments']
)

@router.post(
    "/",
    response_model=EquipmentResponse,
    status_code=201,
    dependencies=[Depends(require_maintenance_manager)],
)
def add_equipment(equipment: RegisterEquipment, db: Session = Depends(get_db)):
    if equipment.department_id is not None:
        department = db.query(Department).filter(Department.id == equipment.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    new_equipment = Equipment(
        type=equipment.type,
        model=equipment.model,
        manufacturer=equipment.manufacturer,
        purchase_date=equipment.purchase_date,
        status=equipment.status.value,
        department_id=equipment.department_id,
    )
    db.add(new_equipment)
    try:
        db.commit()
        db.refresh(new_equipment)
    except:
        db.rollback()
        raise

    return new_equipment

@router.get("/", response_model=List[EquipmentResponse])
def get_equipments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_equipment_read),
):
    
    query = db.query(Equipment)
    if current_user.role == UserRole.REGULAR_STAFF.value:
        query = query.filter(Equipment.assigned_staff_id == current_user.id)
    return query.all()

@router.put(
    "/{equipment_id}",
    response_model=EquipmentResponse,
    dependencies=[Depends(require_maintenance_manager)],
)
def update_equipment(equipment_id: int, equipment: UpdateEquipment, db: Session = Depends(get_db)):
    equip = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equip:
        raise HTTPException(status_code=404, detail="Equipment not found")

    if equipment.department_id is not None:
        department = db.query(Department).filter(Department.id == equipment.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    updates = equipment.model_dump(
        exclude_unset= True,
        mode="json"
    )

    for field, value in updates.items():
        setattr(equip, field, value)

    try:
        db.commit()
        db.refresh(equip)
    except SQLAlchemyError:
        db.rollback()
        raise
    
    return equip

@router.put(
    "/{equipment_id}/assign/{staff_user_id}",
    response_model=EquipmentResponse,
)
def assign_equipment(
    equipment_id: int,
    staff_user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_maintenance_manager),
):
    
    if current_user.department_id is None:
        raise HTTPException(status_code=403, detail="Manager account has no department")
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    staff = db.query(User).filter(User.id == staff_user_id).first()
    if (
        not staff
        or staff.role != UserRole.REGULAR_STAFF.value
        or staff.department_id != current_user.department_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Regular staff member not found in your department",
        )

    equipment.assigned_staff_id = staff.id
    try:
        db.commit()
        db.refresh(equipment)
    except SQLAlchemyError:
        db.rollback()
        raise
    return equipment


@router.delete(
    "/{equipment_id}/assign",
    response_model=EquipmentResponse,
    dependencies=[Depends(require_maintenance_manager)],
)
def unassign_equipment(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    equipment.assigned_staff_id = None
    try:
        db.commit()
        db.refresh(equipment)
    except SQLAlchemyError:
        db.rollback()
        raise
    return equipment


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_equipment_read),
):
    
    query = db.query(Equipment).filter(Equipment.id == equipment_id)
    if current_user.role == UserRole.REGULAR_STAFF.value:
        query = query.filter(Equipment.assigned_staff_id == current_user.id)
    equip = query.first()
    if not equip:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equip