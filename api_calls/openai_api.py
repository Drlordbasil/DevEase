from openai import OpenAI
# Initialize OpenAI
openai = OpenAI()

gpt3 = "gpt-3.5-turbo-16k"
gpt4 = "gpt-4-0125-preview"
model = gpt3

history = ""

def api_calls(user_message, sys_message):
    global history
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": history}
    ]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )
    #history += messages
    history += response.choices[0].message.content
    
    #print("history: ", history)

    return response.choices[0].message.content
