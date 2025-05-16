import os
from openai import OpenAI

print(os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_gpt(user_input, history=None):
    if history is None:
        history = []
    messages = [{"role": "system", "content": "You are a technical interviewer conducting a mock interview."}]

    for h in history:
        messages.append({"role": "user", "content": h['user']})
        messages.append({"role": "assistant", "content": h['ai']})

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo"
        messages=messages
    )

    reply = response.choices[0].message.content
    return reply
