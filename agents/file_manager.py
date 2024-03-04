from api_calls.openai_api import OpenAIAPI
import re

class FileManager:
    def __init__(self):
        self.file = None
        self.openai_api = OpenAIAPI()  # Use clear naming for API instance
    
    def open_file(self, file):
        try:
            with open(f"workspace/{file}", "r") as f:
                self.file = f.read()
            return self.file
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"

    def name_file(self, code):
        name = self.openai_api.api_calls(f"The code is:\n{code}\nCreate a filename with extension as follows only as your response: <filename>.<ext>. ONLY RESPOND WITH A SINGULAR FILENAME!", "You simply create file names that will be saved. If python code is within content, make it .py. if html content, name .html, ect.")
        # Removed the regex validation to trust AI's output directly
        return name.strip()  # Ensure to strip any leading/trailing whitespace
    
    def save_mod_file(self, content):
        file_name = self.name_file(content)
        try:
            with open(f"workspace/{file_name}", "w") as f:
                f.write(content)
            return file_name
        except Exception as e:
            return f"An error occurred while saving the file: {e}"
