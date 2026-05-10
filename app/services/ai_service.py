import json
from google import genai
from google.genai import types
from app.core.config import settings
from app.prompts.coach_prompt import get_system_prompt

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_coach_response(user_profile: dict, chat_history: list, new_message: str):
    system_instruction = get_system_prompt(user_profile)
    
    safety_settings = [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
        ),
    ]

    generation_config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=2048,
        response_mime_type="application/json",
        safety_settings=safety_settings,
        system_instruction=system_instruction
    )

    try:
        contents = []
        for msg in chat_history:
            contents.append({
                "role": msg.role,
                "parts": [{"text": msg.content}]
            })
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents,
            config=generation_config,
            parts=[{"text": new_message}]
        )

        return json.loads(response.text)

    except Exception as e:
        print(f"❌ AI Service Error: {e}")
        return {
            "reply": "عذراً يا بطل، حدث خطأ في معالجة الرد. هل يمكنك إعادة الصياغة؟",
            "suggested_exercises": [],
            "video_urls": []
        }
