
import re
import subprocess
from api_calls.openai_api import OpenAIAPI


def find_pip_installed_packages():
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return result.stdout
libraries = find_pip_installed_packages()
def extract_code(text):
    """
    Extracts Python code from a given text.

    Args:
        text: The text to extract the code from.

    Returns:
        A string containing the extracted Python code.
    """
    pattern = r"```python\n((?:.|\n)*?)```"
    code_blocks = re.findall(pattern, text)
    code = "\n".join(code_blocks)
    code = code.strip()
    return code

class CodeCreator:
    def __init__(self):
        self.create = OpenAIAPI()

    def create_initial_code(self, idea, ceo_feedback):
        persona = "You are a python coding expert. You generate a full script on the first try, removing all # inline comments or placeholders to make the script clear."
        try:
            system_message = persona
            user_message = f"""
            Given the project idea: '{idea}', and the CEO feedback: '{ceo_feedback}', please create an initial Python script that embodies this concept. The script should include the following elements:

            1. Necessary imports: Include any required libraries and modules.
            2. Classes and functions: Define the classes and functions needed to implement the project's functionality.
            3. Main logic: Implement the main logic of the script, ensuring that it is fully functional and adheres to best practices.

            Please format your response using markdown as follows:
            ```python
            # Project Name: [Name of the project]
            # Description: [Brief description of the project]
            # Complete code here without any placeholders or comments
            ```
            Don't put placeholders such as 'pass' in your code. Make sure to remove all comments and placeholders.
            """

            initial_code = self.create.api_calls(user_message, system_message)
            initial_code = extract_code(initial_code)

            return initial_code
        except Exception as e:
            return ""
