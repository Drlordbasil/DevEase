import subprocess
import threading
from tkinter import Tk, PhotoImage, Label, Text, Scrollbar, Button, END, messagebox, VERTICAL, Frame, Canvas, NW
import logging
import re
from datetime import datetime
from api_calls.openai_api import api_calls
from image_creating.image_gen import ImageGen

from agents.feedback_gen import RefinementFeedbackGenerator
from agents.code_creation import CodeCreator
from agents.idea_generator import IdeaGenerator
from agents.adaptive_scripter import AdaptiveScripter
from agents.code_refinement import CodeRefiner
from code_exe import CodeExecutor
from agents.CEO_persona import CEO
from tkinter import messagebox
from agents.career_generator import CareerGenerator
from agents.ai_persona_generator import AIPersonaGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Application:
    def __init__(self, master):
        self.master = master
        master.title("DevEase: Streamlining Development with Ease Utilizing a personal AI army")
        
        # Background image
        self.background_image = PhotoImage(file="assets/background.png")
        self.background_label = Label(master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.log = Text(master, height=25, width=100, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00")


        
        self.setup_buttons()
        self.image_gen = ImageGen()
        self.idea_persona_gen = AIPersonaGenerator()
        
        self.career_gen = CareerGenerator()
        
        self.idea_gen = IdeaGenerator()
        self.code_creator = CodeCreator()
        self.code_exec = CodeExecutor()
        self.code_refiner = CodeRefiner()
        self.adaptive_scripter = AdaptiveScripter()
        self.feedback_gen = RefinementFeedbackGenerator()
        self.CEO = CEO()
        self.career = self.career_gen.generate_career(api_calls)
        self.persona = self.idea_persona_gen.generate_persona(api_calls)
        self.current_idea = ""
        self.current_code = ""  
        self.current_feedback = ""
        self.current_persona = self.persona
        self.current_ceo_message = ""
        self.current_image = ""
        self.current_career = self.career
        self.current_code_output = ""


        self.idea_text, self.idea_scrollbar = self.setup_labeled_text_area("Current Idea", 2, 0)
        self.code_text, self.code_scrollbar = self.setup_labeled_text_area("Current Code", 1, 1)
        self.feedback_text, self.feedback_scrollbar = self.setup_labeled_text_area("Current Feedback", 2, 2)
        self.ceo_message, self.ceo_scrollbar = self.setup_labeled_text_area("CEO Message", 2, 3)
        self.code_output_text, self.code_output_scrollbar = self.setup_labeled_text_area("Current Code Output(to be added)", 2, 1)
        self.career_text, self.career_scrollbar = self.setup_labeled_text_area("Current Career for Idea Gen", 1, 0)
        self.persona_text, self.persona_scrollbar = self.setup_labeled_text_area("Current Persona for Code Gen", 1, 2)






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

        self.generate_idea_button = Button(button_frame, text="Generate Project Idea with initial code", command=self.generate_idea, bg="#111111", fg="#00FF00")
        self.refine_code_button = Button(button_frame, text="Refine Code and get feedback", command=self.refine_code, bg="#111111", fg="#00FF00")
        self.save_final_code_button = Button(button_frame, text="Save Final Code", command=self.save_final_code, bg="#111111", fg="#00FF00")
        self.auto_generate_button = Button(button_frame, text="Auto Generate Program", command=self.on_auto_generate_button_click, bg="#111111", fg="#00FF00")


        self.generate_idea_button.pack(side="left", padx=5, pady=5)
        self.refine_code_button.pack(side="left", padx=5, pady=5)
        self.save_final_code_button.pack(side="left", padx=5, pady=5)
        self.auto_generate_button.pack(padx=5, pady=5)

    def on_adaptive_test_button_click(self):
        threading.Thread(target=AdaptiveScripter().test).start()

    def log_message(self, message):
        self.log.insert(END, message + "\n")
        self.log.see(END)

    def generate_idea(self):
        threading.Thread(target=self._generate_idea_and_code).start()

    def _generate_idea_and_code(self):
        idea = self.idea_gen.generate_idea(api_calls,career=self.career)
        ceo_feedback = self.CEO.review_employee("IdeaGenerator", idea, update_callback=self.log_message)

        if idea:
            self.current_idea = idea  
            
            self.log_message(f"New Idea Generated: {idea}")
            
            if ceo_feedback:
                self.current_ceo_message = ceo_feedback  # Update the current CEO message
                self.log_message(f"CEO Feedback: {ceo_feedback}")
            
            self.update_text_area(self.idea_text, self.current_idea, "Current Idea")
            self.update_text_area(self.ceo_message, self.current_ceo_message, "CEO Message")
            
            self.current_code = self.code_creator.create_initial_code(api_calls, self.persona, self.current_idea)
            self.update_text_area(self.code_text, self.current_code, "Current Code")
            self.current_feedback = self.feedback_gen.generate_feedback(api_calls, self.current_code)
            self.update_text_area(self.feedback_text, self.current_feedback, "Current Feedback")
            self.current_ceo_message = self.CEO.review_employee("CodeCreator", self.current_code, update_callback=self.log_message)
            self.update_text_area(self.ceo_message, self.current_ceo_message, "CEO Message")
            self.update_related_gui_elements()

        else:
            self.log_message("No idea was generated.")

    def update_related_gui_elements(self):
        """Updates related GUI elements to reflect the current state."""
        self.update_text_area(self.persona_text, self.persona, "Current Persona")
        self.update_text_area(self.career_text, self.career, "Current Career")
        self.update_text_area(self.feedback_text, self.current_feedback, "Current Feedback")
        self.update_text_area(self.code_output_text, self.current_code_output, "Current Code Output")
        self.update_text_area(self.ceo_message, self.current_ceo_message, "CEO Message")
        self.update_text_area(self.idea_text, self.current_idea, "Current Idea")
        self.update_text_area(self.code_text, self.current_code, "Current Code")





        
    def refine_code(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to refine.")
            return

        
        self.update_related_gui_elements()
        threading.Thread(target=self._refine_and_execute_code).start()
        self.update_related_gui_elements()



    def _refine_and_execute_code(self):
        """Handles the code refinement and waits for completion before execution."""
        feedback = self.feedback_gen.generate_feedback(api_calls, self.current_code)
        self.current_feedback = feedback if feedback else ""
        self.update_related_gui_elements()
        ceo_message = self.current_ceo_message if self.current_ceo_message else ""
        combined_feedback = f"{feedback} {ceo_message}".strip()
        self.update_related_gui_elements()
        refinement_thread = threading.Thread(target=self.code_refiner.refine_code, args=(self.current_code, combined_feedback, self.log_message))
        refinement_thread.start()
        self.update_related_gui_elements()
        refinement_thread.join()


        self.update_related_gui_elements()

        
        
    def save_final_code(self):
        self.update_text_area(self.code_text, self.current_code)
        self.update_related_gui_elements()
        

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
        self.update_related_gui_elements()
        
        threading.Thread(target=self.generate_feedback).start()
        self.update_text_area(self.feedback_text, self.current_feedback)
        self.current_ceo_message = self.CEO.review_employee("CodeRefiner", self.current_feedback, update_callback=self.log_message)
        self.update_text_area(self.ceo_message, self.current_ceo_message)
        self.update_related_gui_elements()
        


    def auto_generate(self):
        self.update_related_gui_elements()

        t1 = threading.Thread(target=self._generate_idea_and_code)
        t1.start()
        t1.join()
        self.update_related_gui_elements()

        self.log_message("Idea gen complete.")
        self.update_text_area(self.idea_text, self.current_idea, "Current Idea")
        self.update_related_gui_elements()


        
        self.refine_code()
        self.log_message("Refinement complete.")
        self.update_related_gui_elements()

        
        self.log_message("Execution complete.")

        self.save_final_code()
        self.log_message("Save complete.")
        self.update_related_gui_elements()

        self.log_message("Auto generation complete.")
    def on_auto_generate_button_click(self):
        threading.Thread(target=self.auto_generate).start()
        self.update_related_gui_elements()

    def on_exit_button_click(self):
        self.master.quit()
        self.master.destroy()
    def update_text_area(self, text_widget, content, content_description=None):
        text_widget.delete('1.0', END)  # Clear existing content
        if content:
            text_widget.insert(END, content)  
        if content_description:
            self.log_message(f"Updated '{content_description}': {content}")


if __name__ == "__main__":
    root = Tk()
    root.anchor = "center"
    app = Application(root)
    
    root.mainloop()
