from groq import Groq
from app.core.config import settings
from app.prompts.coach_prompt import get_system_prompt
import json
import re

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_coach_response(user_profile: dict, chat_history: list, message: str) -> dict:
    
    
    system_prompt = get_system_prompt(user_profile)

    
    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history:
        
        role = "assistant" if msg.role == "model" else "user"
        messages.append({"role": role, "content": msg.content})

    
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )

        raw_text = response.choices[0].message.content.strip()

         
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return {
                    "reply": data.get("reply", ""),
                    "suggested_exercises": data.get("suggested_exercises", []),
                    "video_urls": data.get("video_urls", []),
                }
            except json.JSONDecodeError:
                pass

        return {
            "reply": raw_text,
            "suggested_exercises": [],
            "video_urls": [],
        }

    except Exception as e:
        return {
            "reply": f"عذراً، حدث خطأ مؤقت. حاول مرة أخرى. ({str(e)})",
            "suggested_exercises": [],
            "video_urls": [],
        }
