
import re
import subprocess

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

    # Define the regular expression pattern for matching Python code blocks
    pattern = r"```python\n((?:.|\n)*?)```"

    # Find all the Python code blocks in the text
    code_blocks = re.findall(pattern, text)

    # Join the code blocks into a single string
    code = "\n".join(code_blocks)

    # Remove the leading and trailing newlines
    code = code.strip()

    return code

class CodeCreator:
    def __init__(self):
        pass

    def create_initial_code(self, api_calls,persona,idea):
        
        try:
            system_message = persona
            user_message = f"""
            Given the project idea: '{idea}', please create an initial Python script that embodies this concept. The script should include the following elements:

            1. Necessary imports: Include any required libraries and modules.
            2. Classes and functions: Define the classes and functions needed to implement the project's functionality.
            3. Main logic: Implement the main logic of the script, ensuring that it is fully functional and adheres to best practices.

            Please format your response using markdown as follows:
            '''python
            # Project Name: [Name of the project]
            # Description: [Brief description of the project]
            # Complete code here without any placeholders or comments
            '''
            """
            
            initial_code = api_calls(user_message, system_message)
            initial_code = extract_code(initial_code)

            return initial_code
        except Exception as e:
            
            return ""
