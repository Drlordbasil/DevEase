from openai import OpenAI
import json
import time
import difflib

class OpenAIAPI:
    def __init__(self, model="gpt-4-0125-preview", history_limit=100):
        self.openai = OpenAI()
        self.model = model
        self.history = []  # Local cache to store history
        self.history_limit = history_limit  # Limit the history size to manage memory efficiently

    def _add_to_history(self, user_message, sys_message, response):
        if len(self.history) >= self.history_limit:
            self.history.pop(0)  # Remove the oldest entry
        self.history.append({
            "timestamp": time.time(),
            "user_message": user_message,
            "sys_message": sys_message,
            "response": response
        })

    def _search_history(self, keyword):
        return [entry for entry in self.history if keyword.lower() in entry['user_message'].lower() or keyword.lower() in entry['response'].lower()]

    def _get_relevant_history(self, user_message):
        """
        Retrieves the most relevant history entries based on the similarity to the current user message.

        Args:
            user_message (str): The current user message.

        Returns:
            list: A list of relevant history entries.
        """
        similarity_scores = [
            (entry, difflib.SequenceMatcher(None, user_message, entry['user_message']).ratio())
            for entry in self.history
        ]
        relevant_entries = [entry for entry, score in similarity_scores if score > 0.5]
        return relevant_entries[-5:]

    def api_calls(self, user_message, sys_message):
        if not isinstance(user_message, str) or not isinstance(sys_message, str):
            raise ValueError("user_message and sys_message must be strings")

        relevant_history = self._get_relevant_history(user_message)
        messages = [
            {"role": "system", "content": sys_message},
            {"role": "user", "content": user_message}
        ] + [
            {"role": "system", "content": entry['sys_message']}
            for entry in relevant_history
        ] + [
            {"role": "user", "content": entry['user_message']}
            for entry in relevant_history
        ]

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0
            )
            response_content = response.choices[0].message.content
            self._add_to_history(user_message, sys_message, response_content)
            return response_content
        except Exception as e:
            raise RuntimeError(f"Failed to make API call: {e}")

    def get_history(self):
        return json.dumps(self.history, indent=4)

    def search_history(self, keyword):
        return json.dumps(self._search_history(keyword), indent=4)
