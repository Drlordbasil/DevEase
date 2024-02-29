
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
Given the project idea: '{idea}', I request the creation of an initial Python script that embodies this concept. 

This script is the foundation of our project, reflecting both the project's ambition and our commitment to quality and innovation in Python programming and give yourself creative freedom.

format your response with markdowns as such:(only answer in this format)
```python
# Project Name: [Name of the project]
# Description: [Brief description of the project]
# complete code here without any placeholders as each function must be fully implemented
# you can use the libraries below
# do not add comments
# do not use placeholders

```

profit and full code > everything else
full code is the only thing that matters when making money
if you dont send full ready-to-use code, you are not making money
if you send full ready-to-use code,
you are making money
you must make money with this code



"""
            
            initial_code = api_calls(user_message, system_message)
            initial_code = extract_code(initial_code)

            return initial_code
        except Exception as e:
            
            return ""
