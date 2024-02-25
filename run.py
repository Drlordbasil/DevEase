import subprocess
import threading
from tkinter import Tk, Text, Scrollbar, Button, END, messagebox, VERTICAL, PhotoImage, Label
import logging
from openai import OpenAI  # Assuming correct setup and import
import re
from datetime import datetime
# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
model = "gpt-3.5-turbo"


# Initialize OpenAI
openai = OpenAI()

def api_calls(user_message, sys_message):
    messages = [
                {"role": "system", "content":sys_message},
                {"role": "user", "content":user_message}
            ]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content


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
class MaestroAI:
    def __init__(self):
        pass
    def generate_career(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def generate_persona(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def generate_feedback(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def generate_idea(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def create_initial_code(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def execute_code(self, user_message, sys_message):
        return api_calls(user_message, sys_message)
    def refine_code(self, user_message, sys_message):
        return api_calls(user_message, sys_message)

class CareerGenerator:
    def __init__(self):
        pass

    def generate_career(self, update_callback):
        try:
            messages = [
                {"role": "system", "content": """
                 
                  You are an extremely analytic and robust AI that was created to help AI developers and programmers with their career paths.
                  You are an AI career advisor and you are advising a Python developer on the best career path
                  to take that allows this person to become an entrepenurial Python developer.
                  You are the best career advisor in the world. 
                  you will inspire them to become rich easily within a short time using AI and Python.
                 
                 """},
                {"role": "user", "content": """
                  I need a career path for a Python developer that is an entrepenuer
                  and likes making money with ease of AI .
                    Give me a name, a brief description of the career, and the skills required that I have. 
                    I need you to give me an entire persona. Have the persona work with nueral networks mainly that generate video or images or content in some form.
                    I need a persona that is a Python developer that is an entrepenuer and likes making money with ease of AI automation in existing technologies.
                 
                    """}
            ]
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3
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
                {"role": "system", "content": """
                 You are an amazingly well known AI prompt engineering specialist giving
                  a persona AKA system message to an AI that will be within a big program. 
                 
                 You are the best prompt engineer for openai based chatbots with system and user messages.
                 Your response is formatted as a system message to an AI that will be within a big program.
                 EXAMPLE RESPONSE:
                 #
                 You are AI that can program anything and everything. You are a Python developer that is an entrepenuer and likes making money with ease of AI automation in existing technologies.
                 #
                 """},
                {"role": "user", "content": """
                 I need a system message for an AI, this AI will be a programmer and the programs it outputs must have multiple classes,
                  use dry method and other professional programming methods to create a singular python based script that automates profit generating.
                  Give me a name, a brief description of the career, and the skills required that I have. I need you to give me an entire persona.
                 
                 """}
            ]
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
            )
            career = response.choices[0].message.content
            update_callback(f"Generated Career: {career}")
            return career
        except Exception as e:
            update_callback(f"Error generating career: {str(e)}")

class RefinementFeedbackGenerator:
    def __init__(self):
        pass

    def generate_feedback(self,code, update_callback):
        try:
            messages = [
                {"role": "system", "content": "Generate feedback for the given Python code. The feedback should be constructive and should help improve the code. You are meticulous and help the other AI team members code."},
                {"role": "user", "content": f"I need feedback for the following Python code. Please provide constructive feedback to help improve the code.{code}"}
            ]
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
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
                {"role": "user", "content": """
                    What's an idea for a project that I can work on that aligns with your career path?
                    I need a robust and innovative idea that will help me become rich easily within a short time using AI and Python.
                 """}
            ]
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
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
                {"role": "user", "content": f"""
                 Given the project idea: '{idea}', write an initial Python script that represents this idea with full robust logic and functions/classes. Send only python script as follows:
                    '''python
                    #name of program and short description
                    #imports
                    #classes and functions
                    #Full program code with imports and classes and real implementations. You are the last line of defense for the code.
                    '''

                 """+idea}
            ]
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
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
            #subprocess.run(["pip", "install", imports], capture_output=True, text=True)
            result = subprocess.run(["python", "temp_code.py"], capture_output=True, text=True, timeout=15)
            feedback = RefinementFeedbackGenerator().generate_feedback(code, update_callback)
            update_callback(f"Feedback: {feedback}")
            if result.returncode == 0:
                update_callback(f"Execution Output: {result.stdout}")
            else:
                update_callback(f"Execution Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            update_callback(f"Code execution timed out.")
            feedback = None
        except Exception as e:
            update_callback(f"An error occurred: {str(e)}")
            feedback = None
        finally:
            return feedback
        


class CodeRefiner:
    def __init__(self):
        pass

    def refine_code(self, code, feedback, update_callback):
        try:
            messages = [
                {"role": "system", "content": """
                 You are a code refinement specialist.
                 You optimize and refine code to make it more efficient and effective.
                 You never leave out code when sending it to the other AI team members.(You are a code refinement specialist for them)
                 You must format your response only with the python code.
                 '''python
                    #name of program and short description
                    #imports
                    #classes and functions
                    #Full program code with imports and classes and real implementations. You are the last line of defense for the code.
                    '''
                 
                 """},
                {"role": "user", "content": f"""
                 Code:\n{code}\nFeedback:\n{feedback}\nPlease refine the code. RULES:
                    #name of program and short description
                    #imports
                    #classes and functions without ANY placeholders such as 'pass' in python
                    # Full program code with imports and classes and real implementations. You are the last line of defense for the code.
                    # you are the last line of defense for the code to be a complete program.
                    # you must send an entire working script
                    # you must never include inline comments or placeholders.
                    # you cant remove any classes or functions unless broken.
                    # you cant make less complex.
                    # you can only make it a robustly coded program with your pride on the line.
                    # check yourself.
                    # make sure you are doing your best.
                    # you can do this.


                 
                 """}
            ]
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
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

        
        self.background_image = PhotoImage(file="assets/background.png")  
        self.background_label = Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
 
        
        self.logo_image = PhotoImage(file="assets/logo.png")  
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
            self.current_feedback = self.code_exec.execute_code(self.current_code, self.log_message)

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
        threading.Thread(target=self.code_exec.execute_code, args=(self.current_code, self.log_message)).start()

    def save_final_code(self):
        

        time = datetime.now().strftime("%Y%m%d%H%M%S")
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to save.")
            return
        file = f"Scripts/final_code{time}.py"
        with open(file, "w") as file:
            file.write(self.current_code)
        
        messagebox.showinfo("Info", f"Final code saved as {file}")

    def generate_feedback(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to generate feedback for.")
            return
        threading.Thread(target=self._generate_feedback).start()

    def auto_generate(self):
        t1 = threading.Thread(target=self._generate_idea_and_code)
        t1.start()
        t1.join()
        self.log_message("Idea gen complete.")

        t2 = threading.Thread(target=self.refine_code)
        t2.start()
        t2.join()
        self.log_message("Refinement 1 complete.")

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
    def on_exit_button_click(self):
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    
    app = Application(root)
    
    root.mainloop()
