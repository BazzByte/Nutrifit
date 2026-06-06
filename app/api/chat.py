from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.chat import Message
from app.models.user import User
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.ai_service import generate_coach_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_coach(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(
            id=1,
            email="default@nutrifit.com",
            hashed_password="placeholder",
            name="Default User"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    user_msg = Message(user_id=user.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    history = db.query(Message).filter(
        Message.user_id == user.id
    ).order_by(Message.timestamp.asc()).limit(10).all()

    ai_result = generate_coach_response({}, history[:-1], request.message)

    model_msg = Message(user_id=user.id, role="model", content=ai_result.get("reply", ""))
    db.add(model_msg)
    db.commit()

    return ChatResponse(
        reply=ai_result.get("reply", "حدث خطأ، حاول مرة أخرى"),
        suggested_exercises=ai_result.get("suggested_exercises", []),
        video_urls=ai_result.get("video_urls", [])
    )
