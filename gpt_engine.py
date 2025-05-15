import openai

openai.api_key = "your_openai_api_key"

def ask_gpt(user_input, history=[]):
    messages = [{"role": "system", "content": "You are a technical interviewer conducting a mock interview."}]
    for h in history:
        messages.append({"role": "user", "content": h['user']})
        messages.append({"role": "assistant", "content": h['ai']})

    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or "gpt-3.5-turbo"
        messages=messages
    )

    reply = response['choices'][0]['message']['content']
    return reply

