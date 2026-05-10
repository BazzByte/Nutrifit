from sqlalchemy import Column, Integer, String, Float, Text
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    goal = Column(String, nullable=True)
    experience_level = Column(String, nullable=True)
    injuries = Column(Text, nullable=True)
    available_equipment = Column(Text, nullable=True)
    dietary_preferences = Column(Text, nullable=True)
