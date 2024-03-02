from openai import OpenAI

class OpenAIAPI:
    def __init__(self, model="gpt-3.5-turbo-16k"):
        self.openai = OpenAI()
        self.model = model
        self.history = []  # Initialize an empty list to store message history

    def api_calls(self, user_message, sys_message, max_history=5):
        """
        Makes API calls to OpenAI chat completions based on user and system messages.
        Efficiently manages history for context retention and searching.

        Args:
            user_message (str): The user's message.
            sys_message (str): The system's message.
            max_history (int): Maximum number of message pairs to retain for context.

        Returns:
            str: The response from the API call.
        """

        if not isinstance(user_message, str) or not isinstance(sys_message, str):
            raise ValueError("user_message and sys_message must be strings")

        # Add the latest system and user messages to the history
        self.history.append({"role": "system", "content": sys_message})
        self.history.append({"role": "user", "content": user_message})

        # Keep the history size within the specified limit
        if len(self.history) > max_history * 2:  # Two entries per interaction
            self.history = self.history[-max_history * 2:]

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=0
            )
        except Exception as e:
            raise RuntimeError("Failed to make API call: " + str(e))

        # Optionally, store the bot's response in history for more contextual future responses
        self.history.append({"role": "assistant", "content": response.choices[0].message.content})

        return response.choices[0].message.content
