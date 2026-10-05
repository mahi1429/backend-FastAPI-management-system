from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class Status(Enum):
    active = "active"
    inactive = "inactive"
    under_maintenance = "under_maintenance"

class RegisterEquipment(BaseModel):
    type: str
    model: str
    manufacturer: str
    purchase_date: date
    status: Status
    department_id: int

class UpdateEquipment(BaseModel):
    status: Optional[Status] = None
    department_id: Optional[int] = None

class EquipmentResponse(BaseModel):
    id: int
    type: str
    model: str
    manufacturer: str
    purchase_date: date
    status: Status
    department_id: int | None
    assigned_staff_id: str | None

    model_config = {
        "from_attributes": True
    }