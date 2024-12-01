#Aplicado engenharia de prompt

from openai import OpenAI
            #Chave de API
client = OpenAI(api_key=' ')

completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": (
            "Você é um desenvolvedor de RPA que usa Playwright com Python para automatizar sites bancários."
        )},
        {
            "role": "user",
            "content": (
                "Desenvolva uma automação RPA para este URL para preencher o arquivo existente.\n"
                "Utilize Playwright com Python."
            )
        }
    ]
)

print(completion.choices[0].message["content"])
