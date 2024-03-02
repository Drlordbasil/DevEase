from api_calls.openai_api import OpenAIAPI


import re
import subprocess
import os
# this class will be responsible for making and running very small scripts for things like scraping a simple page for info or to make changes to a file, like data analysis plugins

class AdaptiveScripter:
    def __init__(self):
        self.create = OpenAIAPI()
    def extract_code(text):
        """
        Extracts Python code from a given text.

        Args:
            text: The text to extract the code from.

        Returns:
            A string containing the extracted Python code.
        """

        # Define the regular expression pattern for matching Python code blocks
        pattern = r"```python\n((?:.|\n)*?)```"

        # Find all the Python code blocks in the text
        code_blocks = re.findall(pattern, text)

        # Join the code blocks into a single string
        code = "\n".join(code_blocks)

        # Remove the leading and trailing newlines
        code = code.strip()

        return code

    def create_script(self, task_needed):
        try:
            
            system_message = """
            You are a python scripter that makes singular class scripts that do a specific task given, you will recieve 
            a task that will need to be translated to a script 
            """

            script = self.create.api_calls(task_needed, system_message)
            print(script)
            return script
        except Exception as e:
            return f"Error generating script: {str(e)}"
    def run_script(self, script):
        try:
            script = self.extract_code(script)
            result = subprocess.run(["python", script], capture_output=True, text=True, timeout=15)
            print(result.stdout)
            return result.stdout
        except Exception as e:
            return f"Error running script: {str(e)}"
    def send_confirmation(self, script):
        try:
            script = self.extract_code(script)
            output = self.run_script(script)
            print(output)
            return f"Script created and ran successfully: {script}{output}"
        except Exception as e:
            return f"Error sending confirmation: {str(e)}"
    def test(self):
        script = self.create_script("scrape this page for this info website is runescape.com and the info is the number of players online right now")
        run = self.run_script(script)
        return self.send_confirmation(script),run
