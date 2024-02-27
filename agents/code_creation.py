
from agents.ai_persona_generator import AIPersonaGenerator
from agents.CEO_persona import CEO
from api_calls.openai_api import api_calls
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

    def create_initial_code(self, idea, update_callback):
        persona = AIPersonaGenerator().generate_persona(update_callback)
        try:
            system_message = persona
            user_message = f"""
Given the project idea: '{idea}', I request the creation of an initial Python script that embodies this concept. 

This script is the foundation of our project, reflecting both the project's ambition and our commitment to quality and innovation in Python programming.

format your response with markdowns as such:(only answer in this format)
```python
# Project Name: [Name of the project]
# Description: [Brief description of the project]
# complete code here
```
you have these libraries you can use:
{libraries}
profit > everything else
you must make money with this code

common error:
    self.model = keras.models.load_model(model_path)

ValueError: File format not supported: filepath=path_to_model. Keras 3 only supports V3 `.keras` files and legacy H5 format files (`.h5` extension). Note that the legacy SavedModel format is not supported by `load_model()` in Keras 3. In order to reload a TensorFlow SavedModel as an inference-only layer in Keras 3, use `keras.layers.TFSMLayer(path_to_model, call_endpoint='serving_default')` (note that your `call_endpoint` might have a different name).
"""
            
            initial_code = api_calls(user_message, system_message)
            initial_code = extract_code(initial_code)
            ceo = CEO()
            ceo_feedback = ceo.review_employee("CodeCreator", initial_code)
            update_callback(f"Initial Code: {initial_code}")
            update_callback(f"Persona: {persona}")
            update_callback(f"Idea: {idea}")
            update_callback(f"current code: {initial_code}")
            return initial_code
        except Exception as e:
            update_callback(f"Error creating initial code: {str(e)}")
            return ""
