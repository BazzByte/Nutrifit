from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from datetime import datetime
from app.database.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # 'user' or 'model'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
