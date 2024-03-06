import threading
from tkinter import messagebox, Tk
from app.agents_manager import AgentManager
from app.ui_components import UIComponents

class Application:
    def __init__(self, master):
        self.master = master
        master.title("DevEase: Streamlining Development with Ease Utilizing a Personal AI Army")
        self.setup_agent_manager()
        self.setup_ui_components()

    def setup_agent_manager(self):
        self.agent_manager = AgentManager()

    def setup_ui_components(self):
        self.ui_components = UIComponents(self.master, self)
        self.current_idea = ""
        self.current_code = ""
        self.current_feedback = ""
        self.current_ceo_message = ""
        self.current_code_output = ""

    def generate_idea(self):
        self.ui_components.disable_buttons()
        try:
            idea = self.agent_manager.generate_idea()
            self.current_idea = idea
            self.ui_components.update_text_area(self.ui_components.idea_text, idea)

            ceo_feedback = self.agent_manager.get_ceo_feedback("IdeaGenerator", idea, self.current_code)
            self.current_ceo_message = ceo_feedback
            self.ui_components.update_text_area(self.ui_components.ceo_message_text, ceo_feedback)

            code = self.agent_manager.code_creator.create_initial_code(idea, ceo_feedback)
            self.current_code = code
            self.ui_components.update_text_area(self.ui_components.code_text, code)
        finally:
            self.ui_components.enable_buttons()

    def refine_code(self):
        self.ui_components.disable_buttons()
        try:
            ceo_feedback = self.agent_manager.get_ceo_feedback("CodeRefiner", self.current_code, "")
            self.current_ceo_message = ceo_feedback
            self.ui_components.update_text_area(self.ui_components.ceo_message_text, ceo_feedback)

            refined_code = self.agent_manager.refine_code(self.current_code, ceo_feedback)
            self.current_code = refined_code
            self.ui_components.update_text_area(self.ui_components.code_text, refined_code)

            code_output = self.agent_manager.analyze_code(refined_code)
            self.current_code_output = code_output
            self.ui_components.update_text_area(self.ui_components.code_output_text, code_output)
        finally:
            self.ui_components.enable_buttons()

    def save_final_code(self):
        self.ui_components.disable_buttons()
        try:
            file_name = self.agent_manager.save_code(self.current_code)
            messagebox.showinfo("Info", f"Final code saved as {file_name}")
        finally:
            self.ui_components.enable_buttons()

    def auto_generate(self):
        self.ui_components.disable_buttons()
        try:
            self.generate_idea()
            self.refine_code()
            self.save_final_code()
        finally:
            self.ui_components.enable_buttons()
            messagebox.showinfo("Info", "Auto generation complete.")

    def get_ceo_feedback(self, agent_name, idea_or_code, additional_info):
        return self.agent_manager.get_ceo_feedback(agent_name, idea_or_code, additional_info)

    def on_exit(self):
        self.master.quit()
        self.master.destroy()