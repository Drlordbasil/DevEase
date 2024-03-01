import re
import subprocess
import threading
from tkinter import Tk, PhotoImage, Label, Text, Scrollbar, Button, END, messagebox, VERTICAL, Frame
import logging
from datetime import datetime

from image_creating.image_gen import ImageGen
from agents.feedback_gen import RefinementFeedbackGenerator
from agents.code_creation import CodeCreator
from agents.idea_generator import IdeaGenerator
from agents.code_refinement import CodeRefiner
from code_exe import CodeExecutor
from agents.CEO_persona import CEO
from api_calls.openai_api import api_calls

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("DevEase: Streamlining Development with Ease Utilizing a personal AI army")
        self.master.state('zoomed')
        self.master.attributes('-fullscreen', True)

        self.text_areas = {}
        self.configure_window()
        self.create_widgets()
        self.initialize_agents()

    def configure_window(self):
        self.background_image = PhotoImage(file="assets/background.png")
        Label(self.master, image=self.background_image).place(x=0, y=0, relwidth=1, relheight=1)
        self.log = Text(self.master, height=25, width=100, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00")
        self.log.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    def create_widgets(self):
        self.setup_buttons()
        self.setup_text_areas()

    def initialize_agents(self):
        self.image_gen = ImageGen()
        self.idea_gen = IdeaGenerator()
        self.code_creator = CodeCreator()
        self.code_exec = CodeExecutor()
        self.code_refiner = CodeRefiner()
        self.feedback_gen = RefinementFeedbackGenerator()
        self.CEO = CEO()

    def setup_buttons(self):
        button_frame = Frame(self.master, background="black")
        button_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        buttons_info = [
            ("Generate Project Idea with initial code", self.generate_idea),
            ("Refine Code and get feedback", self._refine_code),
            ("Save Final Code", self.save_final_code),
            ("Auto Generate Program", self.on_auto_generate_button_click),
        ]
        for text, command in buttons_info:
            Button(button_frame, text=text, command=command, bg="#111111", fg="#00FF00").pack(side="left", padx=5, pady=5)

    def setup_text_areas(self):
        # Configure the weights for the main rows and columns
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # Create a frame for the text areas that will fill the main window
        text_area_frame = Frame(self.master, background="black")
        text_area_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Configure the weights for the text area frame's rows and columns
        text_area_frame.grid_rowconfigure(0, weight=1)  # Current Idea and Code
        text_area_frame.grid_rowconfigure(1, weight=1)  # Feedback and CEO Message
        text_area_frame.grid_columnconfigure(0, weight=1)
        text_area_frame.grid_columnconfigure(1, weight=1)

        # Initialize the text areas with proper grid positioning and spanning
        self.text_areas = {
            "idea": self.create_scrollable_text("Current Idea", 0, 0, text_area_frame),
            "code": self.create_scrollable_text("Current Code", 0, 1, text_area_frame),
            "feedback": self.create_scrollable_text("Current Feedback", 1, 0, text_area_frame),
            "ceo_message": self.create_scrollable_text("CEO Message", 1, 1, text_area_frame),
        }
        self.text_areas["refined_code"] = self.create_scrollable_text("Refined Code", 0, 2, text_area_frame, columnspan=2)

        # The code output text area should span across the bottom two columns
        self.text_areas["code_output"] = self.create_scrollable_text("Code Execution Result", 2, 0, text_area_frame, columnspan=2)
        text_area_frame.grid_rowconfigure(2, weight=1)  # Assign weight for code output row

    def create_scrollable_text(self, label, row, column, parent, columnspan=1):
        frame = Frame(parent, background="black")
        frame.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=5, pady=5)
        Label(frame, text=label, bg="black", fg="#00FF00").grid(row=0, column=0, sticky="ew", columnspan=columnspan)
        text_widget = Text(frame, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00")
        scrollbar = Scrollbar(frame, orient=VERTICAL, command=text_widget.yview)
        text_widget['yscrollcommand'] = scrollbar.set
        text_widget.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        return text_widget

    def generate_idea(self):
        threading.Thread(target=self._generate_idea_and_code).start()

    def _generate_idea_and_code(self):
        idea = self.idea_gen.generate_idea()
        self.update_text_area("idea", idea)

        ceo_feedback = self.CEO.review_employee("CodeCreator", idea, self.update_text_area)
        initial_code = self.code_creator.create_initial_code(idea, ceo_feedback)
        self.update_text_area("code", initial_code)

        self.log_message("Idea and initial code generated successfully.")

    def _refine_code(self):
        code_to_refine = self.text_areas["code"].get("1.0", END)
        feedback = self.feedback_gen.generate_feedback(code_to_refine)
        self.update_text_area("feedback", feedback)
        refined_code = self.code_refiner.refine_code(code_to_refine, feedback)
        self.update_text_area("refined_code", refined_code)  # Update the refined_code text area
        self.log_message("Code refined successfully.")



    def on_auto_generate_button_click(self):
        threading.Thread(target=self.auto_generate).start()

    def auto_generate(self):
        self._generate_idea_and_code()
        self._refine_code()
        self.save_final_code()
        self.log_message("Auto-generation of the program completed.")

    def update_text_area(self, key, content, log_update=True):
        text_widget = self.text_areas[key]
        text_widget.delete('1.0', END)
        text_widget.insert(END, content)
        if log_update:
            self.log_message(f"Updated '{key}': {content}")

    def save_final_code(self):
        code = self.text_areas["code"].get("1.0", END).strip()
        if not code:
            messagebox.showinfo("Info", "No code available to save.")
            return
        threading.Thread(target=self.save_final_code, args=(code)).start()
    def log_message(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - INFO - {message}\n"
        self.log.insert(END, log_entry)
        self.log.see(END)  # Scroll to the end of the log after inserting the message

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
