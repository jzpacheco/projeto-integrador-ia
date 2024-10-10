from openai import OpenAI

client = OpenAI(api_key='')
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a rpa developer who uses playwright with python to develop and maintain banking website automation."},
        {
            "role": "user",
            "content": "Develop a rpa automation to this url to full fill the existing file"
        }
    ]
)

print(completion.choices[0].message)