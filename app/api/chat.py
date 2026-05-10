from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.chat import Message
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.ai_service import generate_coach_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_coach(
    request: ChatRequest,from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.chat import Message
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.ai_service import generate_coach_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_coach(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    user_msg = Message(user_id=1, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    history = db.query(Message).filter(
        Message.user_id == 1
    ).order_by(Message.timestamp.asc()).limit(10).all()

    user_profile = {}

    ai_result = generate_coach_response(user_profile, history[:-1], request.message)

    model_msg = Message(user_id=1, role="model", content=ai_result.get("reply", ""))
    db.add(model_msg)
    db.commit()

    return ChatResponse(
        reply=ai_result.get("reply", "حدث خطأ، حاول مرة أخرى"),
        suggested_exercises=ai_result.get("suggested_exercises", []),
        video_urls=ai_result.get("video_urls", [])
    )
    db: Session = Depends(get_db)
):
    user_msg = Message(user_id=1, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    history = db.query(Message).filter(
        Message.user_id == 1
    ).order_by(Message.timestamp.asc()).limit(10).all()

    user_profile = {
        "name": request.name or "مستخدم",
        "age": request.age,
        "weight": request.weight,
        "height": request.height,
        "goal": request.goal,
        "experience_level": request.experience_level,
        "injuries": request.injuries,
        "available_equipment": request.available_equipment,
        "dietary_preferences": request.dietary_preferences,
    }

    ai_result = generate_coach_response(user_profile, history[:-1], request.message)

    model_msg = Message(user_id=1, role="model", content=ai_result.get("reply", ""))
    db.add(model_msg)
    db.commit()

    return ChatResponse(
        reply=ai_result.get("reply", "حدث خطأ، حاول مرة أخرى"),
        suggested_exercises=ai_result.get("suggested_exercises", []),
        video_urls=ai_result.get("video_urls", [])
    )
