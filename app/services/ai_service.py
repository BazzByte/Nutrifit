import json
from google import genai
from google.genai.types import SafetySetting, HarmCategory, HarmBlockThreshold, GenerateContentConfig
from app.core.config import settings
from app.prompts.coach_prompt import get_system_prompt

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_coach_response(user_profile: dict, chat_history: list, new_message: str):
    system_instruction = get_system_prompt(user_profile)

    safety_settings = [
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH),
    ]

    generation_config = GenerateContentConfig(
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
                "role": msg.role if msg.role in ["user", "model"] else "user",
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
        print(f"AI Error: {str(e)}")
        return {
            "reply": "عذراً , حدث خطأ في معالجة الرد. جرب مرة تانية.",
            "suggested_exercises": [],
            "video_urls": []
        }
