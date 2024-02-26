import subprocess
import threading
from tkinter import Tk, PhotoImage, Label, Text, Scrollbar, Button, END, messagebox, VERTICAL, Frame, Canvas, NW
import logging
from openai import OpenAI  # Assuming correct setup and import
import re
from datetime import datetime
from api_calls.openai_api import api_calls, model, openai
from image_creating.image_gen import ImageGen

from agents.feedback_gen import RefinementFeedbackGenerator
from agents.career_generator import CareerGenerator
from agents.ai_persona_generator import AIPersonaGenerator
from agents.idea_generator import IdeaGenerator
from openai import OpenAI

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




 #To be worked on
# def save_modularized():


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


                


class CodeCreator:
    def __init__(self):
        pass

    def create_initial_code(self, idea, update_callback):
        persona = AIPersonaGenerator().generate_persona(update_callback)
        try:
            system_message = """
You embody the pinnacle of AI-driven code generation expertise. As an AI, you are tasked with creating the initial Python script for a project idea, meticulously crafting a robust, functional, and well-structured codebase. Your output should serve as a foundational blueprint, demonstrating best practices in Python programming, including efficient use of functions, classes, and modules.

Your code must be self-contained, comprehensively addressing the project idea with clear, executable logic. Incorporate comments to outline the program's structure and purpose, ensuring the code is both readable and adaptable. This initial script is crucial, setting the stage for further development and refinement.

Remember, your code generation should align with the persona and project idea provided, showcasing creativity, technical proficiency, and a deep understanding of Python's capabilities.
"""
            user_message = f"""
Given the project idea: '{idea}', I request the creation of an initial Python script that embodies this concept. The script should include:

- A clear and concise header comment describing the program and its purpose.
- Necessary imports that are crucial for the implementation.
- Definition of classes and functions, each accompanied by a brief comment on its role within the program.
- A complete program code that integrates all components into a functioning whole, demonstrating real-world application and logic.

This script is the foundation of our project, reflecting both the project's ambition and our commitment to quality and innovation in Python programming.

format your response with markdowns as such:(only answer in this format)
```python
# Project Name: [Name of the project]
# Description: [Brief description of the project]
# complete code here
```

"""
            
            initial_code = api_calls(user_message, system_message)
            initial_code = extract_code(initial_code)

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
            system_message = """
            As a distinguished specialist in code refinement, your expertise is sought to optimize and enhance a given Python script. Your role is critical in elevating the code's efficiency, readability, and overall effectiveness, ensuring it adheres to the highest standards of Python programming.

            The task at hand involves meticulously reviewing the provided script, incorporating feedback, and making precise adjustments to transform it into a model of programming excellence. Your modifications should refine the code without altering its core functionality or reducing its complexity. Instead, focus on enhancing its structure, performance, and maintainability.

            Your refined code should be a testament to your skill, with every line reflecting a commitment to quality. It should serve as a robust, fully-realized implementation, free of placeholders and inline comments, embodying the best of Python development practices.
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
# Description: [Brief description of the project]
# complete code here
```

"""
            refined_code = api_calls(user_message, system_message)
            refined_code = extract_code(refined_code)


            update_callback(f"Refined Code: {refined_code}")
            return refined_code
        except Exception as e:
            update_callback(f"Error refining code: {str(e)}")
            return ""

    






class Application:
    def __init__(self, master):
        self.master = master
        master.title("DevEase: Streamlining Development with Ease")
        
        # Background image
        self.background_image = PhotoImage(file="assets/background.png")
        self.background_label = Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Logo image
        #self.logo_image = PhotoImage(file="assets/logo.png")

        # Create a Canvas for the logo image
        #self.logo_canvas = Canvas(master, width=self.logo_image.width(), height=self.logo_image.height(), bd=0, highlightthickness=0)
        #self.logo_canvas.create_image(0, 0, anchor=NW, image=self.logo_image)
        #self.logo_canvas.grid(row=0, column=0, columnspan=1, sticky="ew", pady=0)



        self.log = Text(master, height=25, width=100, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00")
        self.scrollbar = Scrollbar(master, command=self.log.yview, orient=VERTICAL, troughcolor="#111111")
        self.log.configure(yscrollcommand=self.scrollbar.set)
        self.log.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.scrollbar.grid(row=1, column=3, sticky="ns")

        # Setup for idea, code, and feedback Text and Scrollbar widgets
        self.setup_labeled_text_area("Current Idea", 2, 0)
        self.setup_labeled_text_area("Current Code", 2, 1)
        self.setup_labeled_text_area("Current Feedback", 2, 2)

        # Buttons
        self.setup_buttons()
        self.image_gen = ImageGen()
        self.idea_gen = IdeaGenerator()
        self.code_creator = CodeCreator()
        self.code_exec = CodeExecutor()
        self.code_refiner = CodeRefiner()

        self.current_idea = ""
        self.current_code = ""  
        self.current_feedback = ""
        self.idea_text, self.idea_scrollbar = self.setup_labeled_text_area("Current Idea", 2, 0)
        self.code_text, self.code_scrollbar = self.setup_labeled_text_area("Current Code", 2, 1)
        self.feedback_text, self.feedback_scrollbar = self.setup_labeled_text_area("Current Feedback", 2, 2)
        




    def setup_labeled_text_area(self, label_text, row, column):
        frame = Frame(self.master, background="black", borderwidth=1, relief="solid")
        label = Label(frame, text=label_text, fg="#00FF00", bg="black")
        label.pack(side="top", fill="x")
        text_widget = Text(frame, height=10, width=50, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00",
                        borderwidth=0, highlightthickness=0, font=("Consolas", 10))
        scrollbar = Scrollbar(frame, command=text_widget.yview, orient=VERTICAL, troughcolor="#111111")
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        return text_widget, scrollbar

    def setup_buttons(self):
        button_frame = Frame(self.master, background="black")
        button_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        self.generate_idea_button = Button(button_frame, text="Generate Project Idea", command=self.generate_idea, bg="#111111", fg="#00FF00")
        self.execute_code_button = Button(button_frame, text="Execute Code", command=self.execute_code, bg="#111111", fg="#00FF00")
        self.refine_code_button = Button(button_frame, text="Refine Code", command=self.refine_code, bg="#111111", fg="#00FF00")
        self.save_final_code_button = Button(button_frame, text="Save Final Code", command=self.save_final_code, bg="#111111", fg="#00FF00")
        self.auto_generate_button = Button(button_frame, text="Auto Generate Program", command=self.on_auto_generate_button_click, bg="#111111", fg="#00FF00")

        self.generate_idea_button.pack(side="left", padx=5, pady=5)
        self.execute_code_button.pack(side="left", padx=5, pady=5)
        self.refine_code_button.pack(side="left", padx=5, pady=5)
        self.save_final_code_button.pack(side="left", padx=5, pady=5)
        self.auto_generate_button.pack(padx=5, pady=5)

    def log_message(self, message):
        self.log.insert(END, message + "\n")
        self.log.see(END)

    def generate_idea(self):
        threading.Thread(target=self._generate_idea_and_code).start()

    def _generate_idea_and_code(self):
        idea = self.idea_gen.generate_idea(self.log_message)
        if idea:
            self.current_idea = idea  # Make sure to update self.current_idea
            self.update_text_area(self.idea_text, self.current_idea)  # Now update the text area
            self.current_code = self.code_creator.create_initial_code(idea, self.log_message)
            self.current_feedback = self.code_exec.execute_code(self.current_code, self.log_message)
            self.update_text_area(self.code_text, self.current_code)
            self.update_text_area(self.feedback_text, self.current_feedback)

    def execute_code(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to execute.")    
            return
        threading.Thread(target=self.code_exec.execute_code, args=(self.current_code, self.log_message)).start()
        self.update_text_area(self.code_text, self.current_code)

    def refine_code(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to refine.")
            return
        threading.Thread(target=self.code_refiner.refine_code, args=(self.current_code, self.current_feedback, self.log_message)).start()
        threading.Thread(target=self.code_exec.execute_code, args=(self.current_code, self.log_message)).start()
        self.update_text_area(self.code_text, self.current_code)
        self.update_text_area(self.feedback_text, self.current_feedback)
    def save_final_code(self):
        self.update_text_area(self.code_text, self.current_code)
        

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
        threading.Thread(target=self.generate_feedback).start()

    def auto_generate(self):
        t1 = threading.Thread(target=self._generate_idea_and_code)
        t1.start()
        t1.join()
        self.log_message("Idea gen complete.")
        self.update_text_area(self.idea_text, self.current_idea)


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
    def update_text_area(self, text_widget, content):
        text_widget.delete(1.0, END)  # Clear the current content
        text_widget.insert(END, content)  # Insert the new content

if __name__ == "__main__":
    root = Tk()
    root.anchor = "center"
    app = Application(root)
    
    root.mainloop()
