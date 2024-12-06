import logging
import os
from openai import OpenAI
from config import settings

logging.basicConfig(level=logging.INFO)

class LLMHandler:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "API key is required to use RPA Auto Fixer. Please set the environment variable OPENAI_API_KEY or pass the API key as a parameter when initializing the library."
            )

    def generate_response(self, code_snippet, html_snippet, traceback_details, func, kwargs):
        
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "Você é um assistente de codificação especializado em corrigir scripts de automação baseados em Playwright. "
                    "Seu objetivo é corrigir problemas encontrados em trechos de código Python fornecidos, baseando-se nos detalhes do erro e no HTML da página. "
                    "Por favor, forneça duas respostas separadas: "
                    "uma explicação do que causou o erro e outra com o código corrigido sem explicações."
                    "Separe a explicação do código com a marcação '### Código corrigido:'."
                    "Não finalize com frases como 'Resto da função permanece inalterado', mas forneça o código completo corrigido."
                    "Ao fim do código corrigido, adicione um bloco if __name__ = '__main__' com a chamada para a função {func} com os kwargs: {kwargs}."
                )},
                {
                "role": "user",
                "content": (
                    "Um erro ocorreu durante a execução de um script de automação RPA. Abaixo estão os detalhes do erro e o trecho de código relevante. "
                    f"Corrija o código para que ele funcione conforme esperado, considerando o traceback e o HTML fornecidos.\n\n "
                    "### Código fornecido:\n"
                    f"```python\n{code_snippet}\n```\n\n"
                    "### HTML da página:\n"
                    f"```html\n{html_snippet}\n```\n\n"
                    "### Detalhes do erro (traceback):\n"
                    f"```\n{traceback_details}\n```"
                )
            }
            ]
        )
        response_content = response.choices[0].message.content
        parts = response_content.split("\n### Código corrigido:")
        
        explanation = parts[0].strip()  # Explicação antes do código
        code_snippet = parts[1].strip() if len(parts) > 1 else ""
        if "```python" in code_snippet and "```" in code_snippet:
            code_start = code_snippet.find("```python") + len("```python\n")
            code_end = code_snippet.find("```", code_start)
            code_snippet = code_snippet[code_start:code_end].strip()

        return explanation, code_snippet