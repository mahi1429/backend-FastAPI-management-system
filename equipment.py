from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped,  mapped_column
from database.base import Base

class Equipment(Base):
    __tablename__ = "equipments"
    id = Column(Integer, primary_key = True)
    type =Column(String, nullable = False)
    model = Column(String, nullable = False)
    manufacturer = Column(String, nullable = False)
    purchase_date = Column(Date, nullable = False)
    status = Column(String, nullable = False)

    department_id = Column(Integer, ForeignKey("departments.id")) 
    assigned_staff_id:  Mapped[str | None] = mapped_column(
        ForeignKey("users.id"),
        nullable = False
        )

    department = relationship("Department", back_populates = "equipments")
    assigned_staff = relationship(
        "User",
        back_populates = "assigned_equipments",
        foreign_keys = [assigned_staff_id]
    )