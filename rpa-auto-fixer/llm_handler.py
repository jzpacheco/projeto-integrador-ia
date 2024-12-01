llm_handler.py



import os
import openai
from config import settings

class LLMHandler:
    def init(self, api_key):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY

        if not self.api_key:
            raise ValueError(
                "API key is required to use RPA Auto Fixer. Please set the environment variable OPENAI_API_KEY or pass the API key as a parameter when initializing the library."
            )

    def generate_response(self, prompt):
        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()