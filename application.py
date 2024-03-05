import threading
from tkinter import Button, Frame, Label, Scrollbar, Text, messagebox, PhotoImage, END, VERTICAL
from tkinter import Tk
from agents.adaptive_scripter import AdaptiveScripter
from agents.code_creation import CodeCreator
from agents.code_refinement import CodeRefiner
from agents.feedback_gen import RefinementFeedbackGenerator
from code_exe import CodeExecutor
from agents.idea_generator import IdeaGenerator
from agents.file_manager import FileManager
from agents.CEO_persona import CEO
from agents.web_research_agent import WebResearch



class Application:
    def __init__(self, master):
        self.master = master
        master.title("DevEase: Streamlining Development with Ease Utilizing a Personal AI Army")
        
        self.setup_background()
        self.setup_log()
        self.setup_buttons()
        self.setup_agents()
        self.setup_text_areas()
        self.setup_collaboration_manager()

    def setup_background(self):
        self.background_image = PhotoImage(file="assets/background.png")
        self.background_label = Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_log(self):
        self.log = Text(self.master, height=10, width=80, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00")
        self.log.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    def setup_buttons(self):
        button_frame = Frame(self.master, background="black")
        button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.generate_idea_button = Button(button_frame, text="Generate Idea", command=self.generate_idea, bg="#111111", fg="#00FF00")
        self.refine_code_button = Button(button_frame, text="Refine Code", command=self.refine_code, bg="#111111", fg="#00FF00")
        self.save_final_code_button = Button(button_frame, text="Save Code", command=self.save_final_code, bg="#111111", fg="#00FF00")
        self.auto_generate_button = Button(button_frame, text="Auto Generate", command=self.on_auto_generate_button_click, bg="#111111", fg="#00FF00")

        self.generate_idea_button.pack(side="left", padx=5, pady=5)
        self.refine_code_button.pack(side="left", padx=5, pady=5)
        self.save_final_code_button.pack(side="left", padx=5, pady=5)
        self.auto_generate_button.pack(side="left", padx=5, pady=5)

    def setup_agents(self):
        self.file_manager = FileManager()
        self.idea_gen = IdeaGenerator()
        self.code_creator = CodeCreator()
        self.code_exec = CodeExecutor()
        self.code_refiner = CodeRefiner()
        self.adaptive_scripter = AdaptiveScripter()
        self.feedback_gen = RefinementFeedbackGenerator()
        self.CEO = CEO()

    def setup_text_areas(self):
        self.current_idea = ""
        self.current_code = ""  
        self.current_feedback = ""
        self.current_ceo_message = ""
        self.current_image = ""
        self.current_code_output = ""

        self.idea_text, self.idea_scrollbar = self.create_text_area("Current Idea", 0, 0)
        self.code_text, self.code_scrollbar = self.create_text_area("Current Code", 0, 1)
        self.feedback_text, self.feedback_scrollbar = self.create_text_area("Current Feedback", 1, 0)
        self.ceo_message, self.ceo_scrollbar = self.create_text_area("CEO Message", 1, 1)
        self.code_output_text, self.code_output_scrollbar = self.create_text_area("Code Execution Result", 2, 0)

    def create_text_area(self, label_text, row, column):
        frame = Frame(self.master, background="black", borderwidth=1, relief="solid")
        label = Label(frame, text=label_text, fg="#00FF00", bg="black")
        label.pack(side="top", fill="x")
        text_widget = Text(frame, height=10, width=40, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00",
                           borderwidth=0, highlightthickness=0, font=("Consolas", 10))
        scrollbar = Scrollbar(frame, command=text_widget.yview, orient=VERTICAL, troughcolor="#111111")
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")
        return text_widget, scrollbar

    def setup_collaboration_manager(self):
        self.agents = {
            "FileManager": self.file_manager,
            "IdeaGenerator": self.idea_gen,
            "CodeCreator": self.code_creator,
            "CodeExecutor": self.code_exec,
            "CodeRefiner": self.code_refiner,
            "AdaptiveScripter": self.adaptive_scripter,
            "FeedbackGenerator": self.feedback_gen,
            "CEO": self.CEO
        }
        self.collaboration_manager = CollaborationManager(self.agents)

    def log_message(self, message):
        self.log.insert(END, message + "\n")
        self.log.see(END)

    def generate_idea(self):
        threading.Thread(target=self._generate_idea_and_code).start()

    def _generate_idea_and_code(self):
        web_research_query = "AI-based project ideas for Python developers that automate profit generation using AI technologies."
        web_research_results = self.collaboration_manager.perform_web_research(web_research_query)
        self.log_message(f"Web Research Results: {web_research_results}")

        idea = self.collaboration_manager.generate_idea()
        ceo_feedback = self.collaboration_manager.get_ceo_feedback("IdeaGenerator", idea, self.current_code)

        if idea:
            self.current_idea = idea  
            self.log_message(f"New Idea Generated: {idea}")
            
            if ceo_feedback:
                self.current_ceo_message = ceo_feedback  
                self.log_message(f"CEO Feedback: {ceo_feedback}")
            
            self.update_text_area(self.idea_text, self.current_idea, "Current Idea")
            self.update_text_area(self.ceo_message, self.current_ceo_message, "CEO Message")
            
            self.current_code = self.code_creator.create_initial_code(self.current_idea, ceo_feedback)
            self.update_text_area(self.code_text, self.current_code, "Current Code")
            self.current_feedback = self.collaboration_manager.generate_feedback(self.current_code)
            self.update_text_area(self.feedback_text, self.current_feedback, "Current Feedback")
            self.current_code_output = self.collaboration_manager.analyze_code(self.current_code)
            self.current_ceo_message = self.collaboration_manager.get_ceo_feedback("CodeCreator: In-charge of Flawless Start Scripts",
                                                                 self.current_code, f"Current Output: {self.current_code_output}")
            self.update_text_area(self.ceo_message, self.current_ceo_message, "CEO Message")
            self.current_code_output = self.collaboration_manager.analyze_code(self.current_code)
            self.update_related_gui_elements()
        else:
            self.log_message("No idea was generated.")

    def update_related_gui_elements(self):
        self.update_gui_elements()

    def refine_code(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to refine.")
            return
        threading.Thread(target=self._refine_and_execute_code, daemon=True).start()

    def _refine_and_execute_code(self):
        feedback = self.collaboration_manager.generate_feedback(self.current_code)
        self.current_feedback = feedback or ""

        self.current_code_output = self.collaboration_manager.analyze_code(self.current_code)
        ceo_message = self.current_ceo_message or ""
        combined_feedback = f"{feedback} {ceo_message} + Here is the output of analysis: {self.current_code_output}".strip()

        refined_code = self.collaboration_manager.refine_code(self.current_code, combined_feedback+f"current output analysis of the code:{self.current_code_output}")
        if refined_code:
            self.current_code = refined_code

        script_task = "Perform data analysis on the generated code"
        script = self.collaboration_manager.generate_script(script_task)
        self.log_message(f"Generated Script: {script}")
        script_output = self.collaboration_manager.run_script(script)
        self.log_message(f"Script Output: {script_output}")
        
        ceo_feedback = self.collaboration_manager.get_ceo_feedback("CodeRefiner", self.current_code, f"Current Output: {self.current_code_output}\nScript Output: {script_output}\n feedback: {combined_feedback} \n remember you are directly chatting with AI so be careful with your words.")
        self.current_ceo_message = ceo_feedback or ""
        self.update_gui_elements()

    def update_gui_elements(self):
        self.update_text_area(self.feedback_text, self.current_feedback, "Current Feedback")
        self.update_text_area(self.code_output_text, self.current_code_output, "Code Execution Result")
        self.update_text_area(self.ceo_message, self.current_ceo_message, "CEO Message")
        self.update_text_area(self.idea_text, self.current_idea, "Current Idea")
        self.update_text_area(self.code_text, self.current_code, "Current Code")

    def save_final_code(self):
        self.update_text_area(self.code_text, self.current_code)
        self.update_related_gui_elements()
        self.current_code_output = self.collaboration_manager.analyze_code(self.current_code)

        file_name = self.collaboration_manager.save_code(self.current_code)
        self.file_name = file_name
        messagebox.showinfo("Info", f"Final code saved as {file_name}")

    def generate_feedback(self):
        if not self.current_code.strip():
            messagebox.showinfo("Info", "No code available to generate feedback for.")
            return
        self.update_related_gui_elements()
        
        threading.Thread(target=self.generate_feedback).start()
        self.update_text_area(self.feedback_text, self.current_feedback)
        self.current_ceo_message = self.collaboration_manager.get_ceo_feedback("CodeRefiner", f"feedback agent response about the code:{self.current_feedback}",
                                                            self.current_code + f"Current Output: {self.current_code_output}")
        self.current_code_output = self.collaboration_manager.analyze_code(self.current_code)
        self.update_text_area(self.ceo_message, self.current_ceo_message)
        self.update_related_gui_elements()

    def auto_generate(self):
        self.update_related_gui_elements()

        t1 = threading.Thread(target=self._generate_idea_and_code)
        t1.start()
        t1.join()
        self.update_related_gui_elements()

        self.log_message("Idea generation complete.")
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
        text_widget.delete('1.0', END)  
        if content:
            text_widget.insert(END, content)  
        if content_description:
            self.log_message(f"Updated '{content_description}': {content}")


class CollaborationManager:
    def __init__(self, agents):
        self.agents = agents
    
    def generate_idea(self):
        return self.agents["IdeaGenerator"].generate_idea()
    
    def get_ceo_feedback(self, agent_name, idea, code):
        return self.agents["CEO"].review_employee(agent_name, idea, code)
    def get_true_false(self,code):
        return self.agents["CEO"].is_code_ready(code)
    
    def generate_feedback(self, code):
        return self.agents["FeedbackGenerator"].generate_feedback(code)
    
    def analyze_code(self, code):
        return self.agents["CodeExecutor"].analyze_code(code)
    
    def refine_code(self, code, feedback):
        return self.agents["CodeRefiner"].refine_code(code, feedback)

    def perform_web_research(self, query):
        web_research = WebResearch()
        web_research.search_google(query)
        results = web_research.get_google_results()
        web_research.close()
        return results

    def generate_script(self, task):
        return self.agents["AdaptiveScripter"].create_script(task)

    def run_script(self, script):
        return self.agents["AdaptiveScripter"].run_script(script)

    def save_code(self, code):
        return self.agents["FileManager"].save_mod_file(code)