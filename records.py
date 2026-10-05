from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from models.record import Record
from models.equipment import Equipment
from models.employee import Employee
from schemas.record import RecordResponse, AddRecord
from security.utils import require_maintenance_manager, require_maintenance_operations

router = APIRouter(
    prefix= "/records",
    tags = ['Records']
)

@router.post(
    "/",
    response_model=RecordResponse,
    status_code=201,
    dependencies=[Depends(require_maintenance_manager)],
)
def add_record(record: AddRecord, db: Session = Depends(get_db)):
    if not db.query(Equipment).filter(Equipment.id == record.equipment_id).first():
        raise HTTPException(status_code=404, detail="Equipment not found")
    if not db.query(Employee).filter(Employee.id == record.employee_id).first():
        raise HTTPException(status_code=404, detail="Employee not found")

    new_record = Record(
        employee_id=record.employee_id,
        equipment_id=record.equipment_id,
        date = record.date,
        problem=record.problem,
        summary=record.summary,
        materials=record.materials,
        cost=record.cost,
        status=record.status
    )
    db.add(new_record)
    try:
        db.commit()
        db.refresh(new_record)
    except:
        db.rollback()
        raise

    return new_record

@router.get(
    "/",
    response_model=List[RecordResponse],
    dependencies=[Depends(require_maintenance_operations)],
)
def get_records(db: Session = Depends(get_db)):
    records = db.query(Record).all()
    return records

@router.get(
    "/{record_id}",
    response_model=RecordResponse,
    dependencies=[Depends(require_maintenance_operations)],
)
def get_record(record_id: int, db: Session = Depends(get_db)):
    rec = db.query(Record).filter(Record.id == record_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    return rec