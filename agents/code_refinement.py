
from api_calls.openai_api import api_calls
import subprocess
import re
def find_pip_installed_packages():
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return result.stdout
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
libraries = find_pip_installed_packages()


class CodeRefiner:
    def __init__(self):
        pass
    
    def refine_code(self, code, feedback, update_callback):
        try:
            system_message = """
            As a distinguished specialist in code refinement, your expertise is sought to optimize and enhance a given Python script. Your role is critical in elevating the code's efficiency, readability, and overall effectiveness, ensuring it adheres to the highest standards of Python programming.

            The task at hand involves meticulously reviewing the provided script, incorporating feedback, and making precise adjustments to transform it into a model of programming excellence. Your modifications should refine the code without altering its core functionality or reducing its complexity. Instead, focus on enhancing its structure, performance, and maintainability.

            Your refined code should be a testament to your skill, with every line reflecting a commitment to quality. It should serve as a robust, fully-realized implementation, free of placeholders and inline comments, embodying the best of Python development practices. direct any code you recieve to profiting stage.
            if you see a comment with info, you must replace with logic to complete the program, if you miss it you can get it next round if needed.
            You are within an iteratively program that is in the process of being refined, and your role is to refine the code to the point where it is a robust and pride-worthy contribution to the project.

            """
            user_message = f"""
I have provided below the initial Python script alongside specific feedback for improvement. Please refine this code according to the following directives:

- Maintain the program's name and a brief description at the beginning.
- Ensure all necessary imports remain, adjusting as needed for optimization.
- Revise classes and functions to eliminate placeholders like 'pass', ensuring each contributes meaningfully to the program's functionality.
- The entire script must be a complete, working program, showcasing advanced Python programming practices without simplification.
- Avoid inline comments or placeholders, aiming for clean and efficient code execution.
- Do not remove any existing classes or functions unless they are fundamentally flawed.
- Strive for excellence, making the code a robust and pride-worthy contribution to our project.

Your expertise in refining this code is invaluable, ensuring it stands as a paragon of Python programming.
feedback: {feedback}
code: {code}
format your response with markdowns as such:(only answer in this format)
```python
# Project Name: [Name of the project]
# complete code here
```
Dont include placeholders, comments or print statements in the final code
This code must be:
- A complete working program
- Free of any syntax errors
- Free of any placeholders
- Free of any inline comments
- profitable and innovative, showcasing the potential of AI and Python as tools for unprecedented automation and innovation.
- Everything it codes must be in full complete code as a single file, and it must be able to run without any errors.
- The code should be a robust and pride-worthy contribution to our project.
- The code should be a testament to your skill, with every line reflecting a commitment to quality.
- It should serve as a robust, fully-realized implementation, free of placeholders and inline comments, embodying the best of Python development practices.
- The code should be a testament to your skill, with every line reflecting a commitment to quality.
you have the following libraries that you can use:
{libraries}
profit > everything else

We need the program running and profiting ASAP.
You are within a company of AI developers and programmers, and your role is to create the initial Python script that will be the foundation of a project. The script should reflect the project's ambition and the company's commitment to quality and innovation in Python programming. The script should be designed to maximize wealth and recognition, showcasing the potential of AI and Python as tools for unprecedented automation and innovation. The name of the company is DevEase, and the AI persona will be integrated into a comprehensive software system.
            The name of the company is DevEase, and the AI persona will be integrated into a comprehensive software system.

"""
            refined_code = api_calls(user_message, system_message)
            refined_code = extract_code(refined_code)
            

            update_callback(f"Refined Code: {refined_code}")
            return refined_code
        except Exception as e:
            update_callback(f"Error refining code: {str(e)}")
            return ""
