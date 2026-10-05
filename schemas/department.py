from pydantic import BaseModel

from schemas.employee import EmployeeResponse
from schemas.equipment import EquipmentResponse


class CreateDepartment(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class DepartmentDetailResponse(DepartmentResponse):
    employees: list[EmployeeResponse]
    equipments: list[EquipmentResponse]