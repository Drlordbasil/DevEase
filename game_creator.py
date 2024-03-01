import re
import os
import subprocess
from api_calls.openai_api import api_calls
from image_creating.image_gen import ImageGen


class CodeUtils:
    def __init__(self):
        pass    

    def install_packages(self, packages):
        os.system(f"pip install {packages}")
        
    def find_pip_installed_packages(self):
        result = subprocess.run(["pip", "list"], capture_output=True, text=True)
        return result.stdout
    
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
    def name_file(self,code):
        name = api_calls(f" The code is {code} Create a filename with ext as follows only as your response: <filename>.<ext>", "You simply create file names that will be saved.")
        return name   
    def save_mod_file(self, content):
        file = self.name_file(content)
        with open(f"Scripts/{file}", "w") as f:
            f.write(content)
        return file
    
class Dynamic_api_agents:
    def __init__(self):
        self.code_utils = CodeUtils()
        self.image_gen = ImageGen()

    def generate_idea(self):
        idea = api_calls("create a kivy based android video game idea in python.", "You are a python coding expert. You generate a full idea that is doable by current AI chatbots. You prompt AI to do it as your response.")
        return idea
    def generate_code(self, idea):
        code = api_calls(f"Create a python script using kivy for android games(dont include custom images since you cant create the images) that will implement the idea: '{idea}' response with markdowns as such '''python <code> '''", "You are a python coding expert. You generate a full script on the first try, removing all # inline comments or placeholders to make the script clear.")
        code = self.code_utils.extract_code(code)
        return code
    def ceo_review(self,idea,code):
        ceo_feedback = api_calls(f"Review the code: '{code}' and the idea: '{idea}' and give feedback.", "You are the CEO of DevEase a program that is full of AI team members, you are the CEO of these team members. You will always direct the AI team to completing their projects quicker and more accurately. Your team cannot create images or sound, so dont ask them to add custom files that arent logic within the script they are working on. They cannot use images that dont exit or sound files.")
        return ceo_feedback
    def refine_code(self, code, ceo_feedback):
        refined_code = api_calls(f"Refine the code:(dont include custom images/paths since you cant create the images) '{code}'(dont include custom images since you cant create the images) with the feedback from your CEO: '{ceo_feedback}'", "You are within an iteratively program that is in the process of being refined, and your role is to refine the code to the point where it is a robust and pride-worthy contribution to the project. You are a coder from DevEase, and you are refining the code to make it more profitable by making it work on first try.")
        return refined_code
    def save_file(self, content):
        file = self.code_utils.save_mod_file(content)
        return file

    
if __name__ == "__main__":
    api = Dynamic_api_agents()
    idea = api.generate_idea()
    print(f"Idea generated: {idea}")
    code = api.generate_code(idea)
    print(f"Code generated: {code}")

    ceo_feedback = api.ceo_review(idea, code)
    print(f"CEO feedback: {ceo_feedback}")
    refined_code = api.refine_code(code, ceo_feedback)
    refined_code = CodeUtils().extract_code(refined_code)
    print(f"Refined code: {refined_code}")
    ceo_feedback = api.ceo_review(idea, refined_code)
    print(f"CEO feedback: {ceo_feedback}")
    refined_code = api.refine_code(refined_code, ceo_feedback)
    refined_code = CodeUtils().extract_code(refined_code)
    print(f"Refined code: {refined_code}")

    file = api.save_file(refined_code)
    print(f"File saved as {file}")
    print(f"Refined code: {refined_code}")