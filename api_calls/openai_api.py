from openai import OpenAI
from news_api import get_news



# Initialize OpenAI
openai = OpenAI()

gpt3 = "gpt-3.5-turbo-16k"
gpt4 = "gpt-4-0125-preview"
model = gpt3


def api_calls(user_message, sys_message):
    """
    Makes API calls to OpenAI chat completions.

    Args:
        user_message (str): The user's message.
        sys_message (str): The system's message.

    Returns:
        str: The response from the API call.
    """
    

    # Validate input
    if not isinstance(user_message, str) or not isinstance(sys_message, str):
        raise ValueError("user_message and sys_message must be strings")
    news = get_news()
    messages = [
        {"role": "system", "content": sys_message},
        #{"role": "assistant", "content": f"here are current news you can read: {news}"},
        {"role": "user", "content": user_message}
       # 
    ]

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
    except Exception as e:
        raise RuntimeError("Failed to make API call: " + str(e))

    #try:
        #history += response.choices[0].message.content
    except (IndexError, AttributeError) as e:
        raise RuntimeError("Failed to update history: " + str(e))

    return response.choices[0].message.content
