from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    suggested_exercises: Optional[List[str]] = []
    video_urls: Optional[List[str]] = []
