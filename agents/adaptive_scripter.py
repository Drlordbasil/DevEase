from api_calls.openai_api import OpenAIAPI
import re
import subprocess
import os

class AdaptiveScripter:
    def __init__(self):
        self.create = OpenAIAPI()

    def extract_code(self, text):
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

    def create_script(self, task_needed, code, idea, ceo_feedback):
        try:
            system_message = """
            You are a python scripter that makes singular class scripts that do a specific task given, you will receive 
            a task that will need to be translated to a script. Consider the current code, idea, and CEO feedback when creating the script.Ensure robust creation as you can generate amazing scripts.
            never include placeholders such as pass in python.            Don't put placeholders such as 'pass' in your code. Make sure to remove all comments and placeholders.
            never use models that dont exist or extensive libraries that may be updated.
            """

            script = self.create.api_calls(task_needed, system_message, code=code, idea=idea, ceo_feedback=ceo_feedback)
            print(script)
            return script
        except Exception as e:
            return f"Error generating script: {str(e)}"

    def run_script(self, script, code_output):
        try:
            script = self.extract_code(script)
            result = subprocess.run(["python", "-c", script], capture_output=True, text=True, timeout=15)
            print(result.stdout)
            return result.stdout
        except Exception as e:
            return f"Error running script: {str(e)}"

    def send_confirmation(self, script, code_output):
        try:
            script = self.extract_code(script)
            output = self.run_script(script, code_output)
            print(output)
            return f"Script created and ran successfully: {script}{output}"
        except Exception as e:
            return f"Error sending confirmation: {str(e)}"

