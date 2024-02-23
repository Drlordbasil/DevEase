import subprocess
import threading
from tkinter import Tk, Text, Scrollbar, Button, END, messagebox, VERTICAL, PhotoImage, Label
import logging
from openai import OpenAI  # Assuming correct setup and import
import re

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI
openai = OpenAI()
def extract_imports_from_code(code):
    """
    Extracts the import statements from a given Python code.

    Args:
        code: The Python code to extract the imports from.

    Returns:
        A list of strings containing the import statements.
    """

    # Define the regular expression pattern for matching import statements
    pattern = r"^\s*import\s+.*$|^\s*from\s+.*\s+import\s+.*$"

    # Find all the import statements in the code
    imports = re.findall(pattern, code, re.MULTILINE)

    return imports
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

class CareerGenerator:
    def __init__(self):
        pass

    def generate_career(self, update_callback):
        try:
            messages = [
                {"role": "system", "content": "Generate a career path for a Python developer. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take. You are an AI career advisor and you are advising a Python developer on the best career path to take."},
                {"role": "user", "content": "I need a career path for a Python developer. Give me a name, a brief description of the career, and the skills required that I have. I need you to give me an entire persona. Have the persona work with nueral networks mainly that generate video or images or content in some form."}
            ]
            response = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0.7
            )
            career = response.choices[0].message.content
            update_callback(f"Generated Career: {career}")
            return career
        except Exception as e:
            update_callback(f"Error generating career: {str(e)}")
            return ""
class AIPersonaGenerator:
    def __init__(self):
        pass

    def generate_persona(self, update_callback):
        try:
            messages = [
                {"role": "system", "content": "You are an amazingly well known AI prompt engineering specialist giving a persona AKA system message to an AI that will be within a big program. You are the best prompt engineer for openai based chatbots with system and user messages."},
                {"role": "user", "content": "I need a system message for an AI, this AI will be a programmer and the programs it outputs must have multiple classes, use dry method and other professional programming methods to create a singular python based script that automates profit generating.. Give me a name, a brief description of the career, and the skills required that I have. I need you to give me an entire persona."}
            ]
            response = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0.7
            )
            career = response.choices[0].message.content
            update_callback(f"Generated Career: {career}")
            return career
        except Exception as e:
            update_callback(f"Error generating career: {str(e)}")

class RefinementFeedbackGenerator:
    def __init__(self):
        pass

    def generate_feedback(self, update_callback):
        try:
            messages = [
                {"role": "system", "content": "Generate feedback for the given Python code. The feedback should be constructive and should help improve the code. You are meticulous and help the other AI team members code."},
                {"role": "user", "content": "I need feedback for the following Python code. Please provide constructive feedback to help improve the code."}
            ]
            response = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0.7
            )
            feedback = response.choices[0].message.content
            update_callback(f"Generated Feedback: {feedback}")
            return feedback
        except Exception as e:
            update_callback(f"Error generating feedback: {str(e)}")
            return ""
                
class IdeaGenerator:
    def __init__(self):
        pass

    def generate_idea(self, update_callback):
        career = CareerGenerator().generate_career(update_callback)
        
        try:
            messages = [
                {"role": "system", "content": career},
                {"role": "user", "content": "I need a project idea for a Python application. Must be a 1 file script that can automate something, but your idea must include a text based flow-chart and You will be sending this to an AI, so prompt engineer your idea."}
            ]
            response = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0.7
            )
            idea = response.choices[0].message.content
            update_callback(f"Generated Idea: {idea}")
            return idea
        except Exception as e:
            update_callback(f"Error generating idea: {str(e)}")
            return ""


class CodeCreator:
    def __init__(self):
        pass

    def create_initial_code(self, idea, update_callback):
        persona = AIPersonaGenerator().generate_persona(update_callback)
        try:
            messages = [
                {"role": "system", "content": persona},
                {"role": "user", "content": f"Given the project idea: '{idea}', write an initial Python script that represents this idea with full robust logic and functions/classes."+idea}
            ]
            response = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0.7
            )
            initial_code = extract_code(response.choices[0].message.content)
            update_callback(f"Initial Code: {initial_code}")
            return initial_code
        except Exception as e:
            update_callback(f"Error creating initial code: {str(e)}")
            return ""


class CodeExecutor:
    def execute_code(self, code, update_callback):
        imports = extract_imports_from_code(code)
        try:
            with open("temp_code.py", "w") as file:
                file.write(code)
            subprocess.run(["pip", "install", imports], capture_output=True, text=True)
            result = subprocess.run(["python", "temp_code.py"], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                update_callback(f"Execution Output: {result.stdout}")
            
            else:
                update_callback(f"Execution Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            update_callback(f"Code execution timed out.{result.stdout}")
        except Exception as e:
            update_callback(f"An error occurred: {str(e)}")


class CodeRefiner:
    def __init__(self):
        pass

    def refine_code(self, code, feedback, update_callback):
        try:
            messages = [
                {"role": "system", "content": "Refine the following Python code based on the feedback. If no feedback, just adapt and assume the code is not working as expected."},
                {"role": "user", "content": f"Code:\n{code}\nFeedback:\n{feedback}\nPlease refine the code."}
            ]
            response = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0.7
            )
            refined_code = extract_code(response.choices[0].message.content)
            update_callback(f"Refined Code: {refined_code}")
            return refined_code
        except Exception as e:
            update_callback(f"Error refining code: {str(e)}")
            return ""

    






class Application:
    def __init__(self, master):
        self.master = master
        master.title("DevEase: Streamlining Development with Ease")

        
        self.background_image = PhotoImage(file="background.png")  
        self.background_label = Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
 
        
        self.logo_image = PhotoImage(file="logo.png")  
        self.logo_label = Label(master, image=self.logo_image)
        self.logo_label.pack(side="top", pady=10)

        self.log = Text(master, height=25, width=100, wrap="word")
        self.scrollbar = Scrollbar(master, command=self.log.yview, orient=VERTICAL)
        self.log.configure(yscrollcommand=self.scrollbar.set, bg="white", fg="black")
        self.log.pack(side="left", fill="y")
        self.scrollbar.pack(side="left", fill="y")

        self.idea_gen = IdeaGenerator()
        self.code_creator = CodeCreator()
        self.code_exec = CodeExecutor()
        self.code_refiner = CodeRefiner()

        self.generate_idea_button = Button(master, text="Generate Project Idea and initial script", command=self.generate_idea)
        self.generate_idea_button.pack(pady=5)

        self.execute_code_button = Button(master, text="Execute current Code", command=self.execute_code)
        self.execute_code_button.pack(pady=5)

        self.refine_code_button = Button(master, text="Refine Current Code", command=self.refine_code)
        self.refine_code_button.pack(pady=5)
        
        self.save_final_code_button = Button(master, text="Save current code as Final Code", command=self.save_final_code)
        self.save_final_code_button.pack(pady=5)

        self.auto_generate_button = Button(master, text="Auto Generate Program on Idea generated", command=self.on_auto_generate_button_click)
        self.auto_generate_button.pack(pady=5)

        self.current_idea = ""
        self.current_code = ""  
        self.current_feedback = ""

    def log_message(self, message):
        self.log.insert(END, message + "\n")
        self.log.see(END)

    def generate_idea(self):
        threading.Thread(target=self._generate_idea_and_code).start()

    def _generate_idea_and_code(self):
        idea = self.idea_gen.generate_idea(self.log_message)
        if idea:
            self.current_code = self.code_creator.create_initial_code(idea, self.log_message)

    def execute_code(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to execute.")
            return
        threading.Thread(target=self.code_exec.execute_code, args=(self.current_code, self.log_message)).start()

    def refine_code(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to refine.")
            return
        threading.Thread(target=self.code_refiner.refine_code, args=(self.current_code, self.current_feedback, self.log_message)).start()

    def save_final_code(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to save.")
            return
        with open("final_code.py", "w") as file:
            file.write(self.current_code)
        messagebox.showinfo("Info", "Final code saved as final_code.py")


    def auto_generate(self):
        t1 = threading.Thread(target=self._generate_idea_and_code)
        t1.start()
        t1.join()
        self.log_message("Idea gen complete.")

        t2 = threading.Thread(target=self.refine_code)
        t2.start()
        t2.join()
        self.log_message("Refinement complete.")

        t3 = threading.Thread(target=self.execute_code)
        t3.start()
        t3.join()
        self.log_message("Execution complete.")

        t4 = threading.Thread(target=self.save_final_code)
        t4.start()
        t4.join()
        self.log_message("Save complete.")

        self.log_message("Auto generation complete.")
    def on_auto_generate_button_click(self):
        threading.Thread(target=self.auto_generate).start()

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    
    root.mainloop()
