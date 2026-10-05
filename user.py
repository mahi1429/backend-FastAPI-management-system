from pydantic import BaseModel, EmailStr, model_validator

from models.user import UserRole


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole
    department_id: int | None = None

    @model_validator(mode="after")
    def validate_department_for_maintenance_roles(self):
        maintenance_roles = {
            UserRole.MAINTENANCE_MANAGER,
            UserRole.MAINTENANCE_SUPERVISOR,
            UserRole.REGULAR_STAFF,
        }
        if self.role in maintenance_roles and self.department_id is None:
            raise ValueError("Maintenance accounts must be assigned to a department")
        return self

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: UserRole
    department_id: int | None

    model_config = {
        "from_attributes": True
    }