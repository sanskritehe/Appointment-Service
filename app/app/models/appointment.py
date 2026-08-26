from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
