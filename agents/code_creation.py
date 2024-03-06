import re
import subprocess
from api_calls.openai_api import OpenAIAPI
import ast
import logging

def find_pip_installed_packages():
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return result.stdout

def extract_code(text):
    pattern = r"```python\n((?:.|\n)*?)```"
    code_blocks = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
    code = "\n".join(code_blocks)
    code = code.strip()
    return code

class CodeCreator:
    def __init__(self):
        self.openai_api = OpenAIAPI()
        self.installed_packages = find_pip_installed_packages()
        logging.basicConfig(filename='code_creator.log', level=logging.INFO)

    def create_initial_code(self, idea, ceo_feedback):
        logging.info(f"Creating initial code for idea: {idea}")
        persona = "You are a Python coding expert. You generate a full script on the first try, optimizing for profitability and aligning with market demands."

        system_message = f"{persona}"

        user_message = f"""
        Given the project idea: '{idea}', and the CEO feedback: '{ceo_feedback}', please create an initial Python script that embodies this concept. The script should include the following elements:

        1. Necessary imports: Include any required libraries and modules, considering the installed packages: {self.installed_packages}
        2. Classes and functions: Define the classes and functions needed to implement the project's functionality, following best practices and design principles.
        3. Main logic: Implement the main logic of the script, ensuring that it is fully functional, efficient, and optimized for profitability.
        4. Error handling and logging: Incorporate appropriate error handling and logging mechanisms to ensure robustness and maintainability.
        5. Documentation: Include docstrings and comments to document the code's purpose, inputs, outputs, and any important considerations.

        Please format your response using markdown as follows:
        ```python
        # Project Name: [Name of the project]
        # Description: [Brief description of the project]
        # Complete code here
        ```
        """

        try:
            initial_code = self.openai_api.api_calls(user_message, system_message)
            initial_code = extract_code(initial_code)
            logging.info("Initial code created successfully.")

            if initial_code:
                try:
                    ast.parse(initial_code)
                    logging.info("Code is syntactically valid.")
                except SyntaxError as e:
                    logging.error(f"Syntax error in generated code: {e}")
                    initial_code = self.fix_syntax_errors(initial_code)

                initial_code = self.format_code(initial_code)
                logging.info("Code formatting completed.")

            return initial_code
        except Exception as e:
            logging.error(f"Error creating initial code: {e}")
            return ""

    def fix_syntax_errors(self, code):
        logging.info("Fixing syntax errors in the code.")
        fixed_code = self.openai_api.api_calls(f"Fix the syntax errors in the following Python code:\n\n{code}", "You are a Python syntax error fixer.")
        return fixed_code.strip()

    def format_code(self, code):
        logging.info("Formatting the code.")
        formatted_code = self.openai_api.api_calls(f"Format the following Python code according to PEP 8 guidelines:\n\n{code}", "You are a Python code formatter.")
        return formatted_code.strip()