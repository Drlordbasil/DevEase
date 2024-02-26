from openai import OpenAI

# Initialize OpenAI
openai = OpenAI()
model = "gpt-4-0125-preview"


history = ""

def api_calls(user_message, sys_message):
    global history
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": history+user_message}
    ]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )
    history += response.choices[0].message.content
    #print("history: ", history)

    return response.choices[0].message.content
