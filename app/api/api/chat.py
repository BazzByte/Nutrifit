from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.chat import Message
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.api.auth import get_current_user
from app.services.ai_service import generate_coach_response

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_coach(
    request: ChatRequest, 
    current_user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # حفظ رسالة المستخدم
    user_msg = Message(user_id=current_user.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # جلب آخر 10 رسائل
    chat_history = db.query(Message).filter(
        Message.user_id == current_user.id
    ).order_by(Message.timestamp.asc()).limit(10).all()

    # بروفايل المستخدم
    user_profile = {
        "name": current_user.name,
        "age": current_user.age,
        "weight": current_user.weight,
        "height": current_user.height,
        "goal": current_user.goal,
        "experience_level": current_user.experience_level,
        "injuries": current_user.injuries,
        "available_equipment": current_user.available_equipment,
        "dietary_preferences": current_user.dietary_preferences
    }

    # استدعاء AI
    ai_result = generate_coach_response(user_profile, chat_history[:-1], request.message)

    # حفظ رد الـ AI
    model_msg = Message(user_id=current_user.id, role="model", content=ai_result.get("reply", ""))
    db.add(model_msg)
    db.commit()

    return ChatResponse(
        reply=ai_result.get("reply", "حدث خطأ، حاول مرة أخرى"),
        suggested_exercises=ai_result.get("suggested_exercises", []),
        video_urls=ai_result.get("video_urls", [])
    )
