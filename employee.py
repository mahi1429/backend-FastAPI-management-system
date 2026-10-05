from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key = True)
    name = Column(Integer, nullable = False)
    email = Column(String, unique = True, nullable = False)
    birth_date = Column(Date)
    
    department_id = Column(String, ForeignKey("departments.id"), nullable = False)
    department = relationship("Department", back_populates = "employee")

