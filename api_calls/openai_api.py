from openai import OpenAI

# Initialize OpenAI
openai = OpenAI()
model = "gpt-3.5-turbo-16k"


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
