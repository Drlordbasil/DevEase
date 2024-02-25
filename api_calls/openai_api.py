# Initialize OpenAI

from openai import OpenAI
openai = OpenAI()

def api_calls(user_message, sys_message):
    messages = [
                {"role": "system", "content":sys_message},
                {"role": "user", "content":user_message}
            ]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content
