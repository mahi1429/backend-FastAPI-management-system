from pydantic import BaseModel
from datetime import date

class AddRecord(BaseModel):
    employee_id: int
    equipment_id: int
    date: date
    problem: str
    summary: str
    materials: str
    cost: float
    status: str

class RecordResponse(BaseModel):
    id: int
    employee_id: int
    equipment_id: int
    date: date
    problem: str
    summary: str
    materials: str
    cost: float
    status: str

    model_config = { 
        "from_attributes": True
    }
