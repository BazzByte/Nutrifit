from google import genai
from google.genai import types
from app.core.config import settings
import os

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.0-flash"   

    def generate_response(self, prompt: str, context: str = None) -> str:
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt

            response = self.client.models.generate_content(
                model=self.model,
                contents=[full_prompt]
            )
            
            return response.text if response.text else "Sorry, I couldn't generate a response."

        except Exception as e:
            print("❌ Gemini API Error:")
            import traceback
            print(traceback.format_exc())
            return "حدث خطأ أثناء توليد الرد. برجاء المحاولة مرة أخرى."

    def generate_nutrition_plan(self, user_data: dict) -> str:
        prompt = f"""
        أنشئ خطة تغذية يومية مفصلة للشخص التالي:
        الاسم: {user_data.get('name')}
        العمر: {user_data.get('age')}
        الوزن: {user_data.get('weight')} كجم
        الطول: {user_data.get('height')} سم
        الهدف: {user_data.get('goal')}
        المعدات المتوفرة: {user_data.get('available_equipment')}
        """
        
        return self.generate_response(prompt)
