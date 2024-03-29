from openai import OpenAI
import json
import time
import difflib
import tiktoken

gpt3 = "gpt-3.5-turbo-16k"
gpt4 = "gpt-4-0125-preview"
token_context_windows = {
    gpt3: 16000,
    gpt4: 128000,
}

class OpenAIAPI:
    def __init__(self, model=gpt3, history_limit=10):
        self.openai = OpenAI()
        self.model = model
        self.history = []
        self.history_limit = history_limit

    def _add_to_history(self, user_message, sys_message, response):
        if len(self.history) >= self.history_limit:
            self.history.pop(0)
        self.history.append({
            "timestamp": time.time(),
            "user_message": user_message,
            "sys_message": sys_message,
            "response": response
        })

    def _search_history(self, keyword):
        return [entry for entry in self.history if keyword.lower() in entry['user_message'].lower() or keyword.lower() in entry['response'].lower()]

    def _get_relevant_history(self, user_message):
        similarity_scores = [
            (entry, difflib.SequenceMatcher(None, user_message, entry['user_message']).ratio())
            for entry in self.history
        ]
        relevant_entries = [entry for entry, score in similarity_scores if score > 0.5]
        return relevant_entries[-10:]  # Increase the number of relevant entries to 10

    def _ensure_token_limit(self, messages, model):
        max_tokens = token_context_windows.get(model, 16000)
        total_tokens = num_tokens_from_messages(messages, model)
        while total_tokens > max_tokens:
            messages.pop(0)
            total_tokens = num_tokens_from_messages(messages, model)
        return messages

    def api_calls(self, user_message, sys_message, code_context=None):
        if not isinstance(user_message, str) or not isinstance(sys_message, str):
            raise ValueError("user_message and sys_message must be strings")
        
        relevant_history = self._get_relevant_history(user_message)
        
        messages = [{"role": "system", "content": sys_message}, {"role": "user", "content": user_message}]
        
        if code_context:
            messages.insert(1, {"role": "system", "content": f"Code Context:\n{code_context}"})  # Add code context to the messages
        
        messages.extend([{"role": role, "content": entry[role + '_message']} for entry in relevant_history for role in ["system", "user"] if role + '_message' in entry])
        
        messages = self._ensure_token_limit(messages, self.model)
        
        try:
            response = self.openai.chat.completions.create(model=self.model, messages=messages, temperature=0)
            response_content = response.choices[0].message.content
            self._add_to_history(user_message, sys_message, response_content)
            return response_content
        except Exception as e:
            raise RuntimeError(f"Failed to make API call: {e}")

    def get_history(self):
        return json.dumps(self.history, indent=4)

    def search_history(self, keyword):
        return json.dumps(self._search_history(keyword), indent=4)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens -= 1
        num_tokens += 2
    return num_tokens