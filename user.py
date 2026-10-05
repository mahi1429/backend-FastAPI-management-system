from enum import Enum
import uuid
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from database.base import Base

class UserRole(str, Enum):
    HR = "hr"
    MAINTENANCE_MANAGER = "maintenance_manager"
    MAINTENANCE_SUPERVISOR = "maintenance_supervisor"
    REGULAR_STAFF = "regular_staff"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=UserRole.REGULAR_STAFF.value,
    )
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"),
        nullable=True,
    )

    department = relationship("Department", back_populates="users")
    assigned_equipments = relationship(
        "Equipment",
        back_populates="assigned_staff",
        foreign_keys="Equipment.assigned_staff_id",
    )