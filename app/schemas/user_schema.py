from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: str                          
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    goal: Optional[str] = None
    experience_level: Optional[str] = None
    injuries: Optional[str] = None
    available_equipment: Optional[str] = None
    dietary_preferences: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    name: str

    class Config:
        from_attributes = True
