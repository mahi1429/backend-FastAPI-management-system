from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class RegisterEmployee(BaseModel):
    name: str
    email: EmailStr
    birth_date: date
    department_id: int | None = None

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    birth_date: date
    department_id: int | None

    model_config = {
        "from_attributes": True
    }