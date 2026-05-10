from google import genai
from app.core.config import settings

_client = None

def get_ai_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY.strip() == "":
            print("❌ GEMINI_API_KEY is missing!")
            raise ValueError("GEMINI_API_KEY is not set in environment variables")
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def generate_coach_response(user_profile: dict, chat_history: list, new_message: str):
    try:
        client = get_ai_client()
        return {"reply": "اقدر اساعدك ازاي؟"}
    except Exception as e:
        print("❌ AI Error:", str(e))
        import traceback
        print(traceback.format_exc())
        return {"reply": "عذراً، حدث خطأ. جرب مرة أخرى."}
