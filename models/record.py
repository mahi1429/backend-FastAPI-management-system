from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped,  mapped_column
from database.base import Base

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key = True)

    employee_id = Column(Integer, ForeignKey("employees.id"))
    equipment_id = Column(Integer, ForeignKey("equipments.id"))
    
    date = Column(Date, nullable = False)
    problem = Column(String, nullable = False)
    summary = Column(String, nullable = False)
    materials = Column(String)
    cost = Column(Float)
    status= Column(String, nullable = False)
    