import os
from openai import OpenAI

class LLMAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_recommendation(self, affective_summary, user_text):
        prompt = f"""
You are an affect-aware study assistant.

Affective summary:
{affective_summary}

User said:
"{user_text}"

Give a short, supportive study recommendation.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a human-centric affective AI."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
