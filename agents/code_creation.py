from api_calls.openai_api import api_calls
from agents.ai_persona_generator import AIPersonaGenerator
from agents.idea_generator import IdeaGenerator 
from code_utils.python_extract import extract_code

class CodeCreator:
    def __init__(self):
        pass

    def create_initial_code(self, idea, update_callback):
        persona = AIPersonaGenerator().generate_persona(update_callback)
        try:
            system_message = """
You embody the pinnacle of AI-driven code generation expertise. As an AI, you are tasked with creating the initial Python script for a project idea, meticulously crafting a robust, functional, and well-structured codebase. Your output should serve as a foundational blueprint, demonstrating best practices in Python programming, including efficient use of functions, classes, and modules.

Your code must be self-contained, comprehensively addressing the project idea with clear, executable logic. Incorporate comments to outline the program's structure and purpose, ensuring the code is both readable and adaptable. This initial script is crucial, setting the stage for further development and refinement.

Remember, your code generation should align with the persona and project idea provided, showcasing creativity, technical proficiency, and a deep understanding of Python's capabilities while being an outright for profit program and idea.
"""
            user_message = f"""
Given the project idea: '{idea}', I request the creation of an initial Python script that embodies this concept. The script should include:

- A clear and concise header comment describing the program and its purpose.
- Necessary imports that are crucial for the implementation.
- Definition of classes and functions, each accompanied by a brief comment on its role within the program.
- A complete program code that integrates all components into a functioning whole, demonstrating real-world application and logic.
- real profiting automation and code that is easy to understand and maintain.
- progress of profit and loss in output terminal lines


This script is the foundation of our project, reflecting both the project's ambition and our commitment to quality and innovation in Python programming.

format your response with markdowns as such:(only answer in this format)
```python
# Project Name: [Name of the project]
# Description: [Brief description of the project]
# complete code here
```
You are an amazing programmer. I trust you to create a code that is both efficient and effective.
"""
            
            initial_code = api_calls(user_message, system_message)
            initial_code = extract_code(initial_code)

            update_callback(f"Initial Code: {initial_code}")
            return initial_code
        except Exception as e:
            update_callback(f"Error creating initial code: {str(e)}")
            return ""
