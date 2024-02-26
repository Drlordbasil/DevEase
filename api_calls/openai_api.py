from openai import OpenAI

# Initialize OpenAI
openai = OpenAI()

gpt3 = "gpt-3.5-turbo-16k"
gpt4 = "gpt-4-0125-preview"
model = gpt4

history = ""

def api_calls(user_message, sys_message):
    global history

    # Validate input
    if not isinstance(user_message, str) or not isinstance(sys_message, str):
        raise ValueError("user_message and sys_message must be strings")

    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": history}
    ]

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3
        )
    except Exception as e:
        raise RuntimeError("Failed to make API call: " + str(e))

    try:
        history += response.choices[0].message.content
    except (IndexError, AttributeError) as e:
        raise RuntimeError("Failed to update history: " + str(e))

    return response.choices[0].message.content
