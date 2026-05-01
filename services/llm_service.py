# services/llm_service.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL")

        if not api_key or not self.model:
            raise ValueError("Groq env variables missing")

        self.client = Groq(api_key=api_key)

    def generate(self, query, context):
        prompt = f"""
You are a helpful assistant.

Use ONLY the context below to answer.
If answer is not present, say "I don't know".

Context:
{context}

Question:
{query}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content