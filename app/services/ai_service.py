import google.generativeai as genai
import json
from app.core.config import settings
from app.prompts.coach_prompt import get_system_prompt

genai.configure(api_key=settings.GEMINI_API_KEY)

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]

def generate_coach_response(user_profile: dict, chat_history: list, new_message: str):
    system_instruction = get_system_prompt(user_profile)
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction,
        safety_settings=safety_settings,
        generation_config={"response_mime_type": "application/json"}
    )

    formatted_history = [{"role": msg.role, "parts": [msg.content]} for msg in chat_history]
    
    chat = model.start_chat(history=formatted_history)
    response = chat.send_message(new_message)
    
    try:
        return json.loads(response.text)
    except:
        return {
            "reply": "عذراً، حدث خطأ في معالجة الرد. حاول مرة أخرى.",
            "suggested_exercises": [],
            "video_urls": []
        }
