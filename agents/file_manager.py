from api_calls.openai_api import OpenAIAPI

import re

class FileManager:
    def __init__(self):
        self.file = None
        self.create = OpenAIAPI()
    def open_file(self, file):
        with open(f"workspace/{file}", "r") as f:
            self.file = f.read()
        return self.file
    def name_file(self,code):
        
        name = self.create.api_calls(f" The code is {code} Create a filename with ext as follows only as your response: <filename>.<ext> ONLY RESPOND WITH A SINGULAR FILENAME!", "You simply create file names that will be saved.")
        return name   
    def save_mod_file(self, content):
        file = self.name_file(content)
        with open(f"workspace/{file}", "w") as f:
            f.write(content)
        return file
