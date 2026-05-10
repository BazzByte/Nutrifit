from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    goal: Optional[str] = None
    experience_level: Optional[str] = None
    injuries: Optional[str] = None
    available_equipment: Optional[str] = None
    dietary_preferences: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    suggested_exercises: Optional[List[str]] = []
    video_urls: Optional[List[str]] = []
