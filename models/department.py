from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.base import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

    employees = relationship("Employee", back_populates = "department")
    equipments = relationship("Equipment", back_populates = "department")
    

