import json
import re
from google import genai
from app.core.config import settings
from app.prompts.coach_prompt import get_system_prompt
 
client = genai.Client(api_key=settings.GEMINI_API_KEY)
 
def generate_coach_response(user_profile: dict, chat_history: list, user_message: str) -> dict:
    try:
        system_prompt = get_system_prompt(user_profile)
 
       history = []
        for msg in chat_history:
            role = "user" if msg.role == "user" else "model"
            history.append({"role": role, "parts": [{"text": msg.content}]})
 
        full_message = f"{system_prompt}\n\nرسالة المستخدم: {user_message}"
 
        contents = history + [{"role": "user", "parts": [{"text": full_message}]}]
 
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )
 
        raw_text = response.text.strip()
 
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return {
                "reply": result.get("reply", raw_text),
                "suggested_exercises": result.get("suggested_exercises", []),
                "video_urls": result.get("video_urls", []),
            }
 
        return {
            "reply": raw_text,
            "suggested_exercises": [],
            "video_urls": [],
        }
 
    except Exception as e:
        print(f"❌ AI Service Error: {e}")
        return {
            "reply": "عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي. حاول مرة أخرى.",
            "suggested_exercises": [],
            "video_urls": [],
        }
