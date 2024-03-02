import subprocess
import threading
from tkinter import Tk, PhotoImage, Label, Text, Scrollbar, Button, END, messagebox, VERTICAL, Frame
import logging
from queue import Queue
from tkinter import simpledialog

from image_creating.image_gen import ImageGen
from agents.feedback_gen import RefinementFeedbackGenerator
from agents.code_creation import CodeCreator
from agents.idea_generator import IdeaGenerator
from agents.adaptive_scripter import AdaptiveScripter
from agents.code_refinement import CodeRefiner
from code_exe import CodeExecutor
from agents.CEO_persona import CEO
from agents.file_manager import FileManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DevEaseApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("DevEase: Enhancing Development with AI")

        self.bgImage = PhotoImage(file="assets/background.png")
        self.bgLabel = Label(master, image=self.bgImage)
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.logArea = Text(master, height=25, width=100, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00")

        self.queue = Queue()
        self.master.after(100, self.processQueue)

        self.initializeUIComponents()
        self.setupAgents()
        self.clearState()

    def setupAgents(self):
        self.imageGenerator = ImageGen()
        self.fileSaver = FileManager()
        self.ideaGenerator = IdeaGenerator()
        self.codeGenerator = CodeCreator()
        self.codeRunner = CodeExecutor()
        self.codeOptimizer = CodeRefiner()
        self.scripter = AdaptiveScripter()
        self.feedbackProvider = RefinementFeedbackGenerator()
        self.ceoAdvisor = CEO()

    def clearState(self):
        self.idea = ""
        self.code = ""
        self.feedback = ""
        self.ceoFeedback = ""
        self.executionOutput = ""

    def initializeUIComponents(self):
        self.setupTextAreas()
        self.setupActionButtons()

    def setupTextAreas(self):
        self.ideaArea, _ = self.createTextSection("Idea", 2, 0)
        self.codeArea, _ = self.createTextSection("Code", 2, 2)
        self.feedbackArea, _ = self.createTextSection("Feedback", 1, 1)
        self.ceoMessageArea, _ = self.createTextSection("CEO Feedback", 2, 3)
        self.executionResultArea, _ = self.createTextSection("Execution Result", 2, 1)

    def createTextSection(self, title, row, col):
        container = Frame(self.master, background="black", borderwidth=1, relief="solid")
        Label(container, text=title, fg="#00FF00", bg="black").pack(side="top", fill="x")
        textWidget = Text(container, height=10, width=50, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00", font=("Consolas", 10))
        scroll = Scrollbar(container, command=textWidget.yview, orient=VERTICAL)
        textWidget.configure(yscrollcommand=scroll.set)
        textWidget.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        container.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        return textWidget, scroll

    def setupActionButtons(self):
        actionPanel = Frame(self.master, background="black")
        actionPanel.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        self.ideaBtn = Button(actionPanel, text="Generate Idea", command=self.triggerIdeaGeneration, bg="#111111", fg="#00FF00")
        self.refineBtn = Button(actionPanel, text="Refine Code", command=self.refineCode, bg="#111111", fg="#00FF00")
        self.saveBtn = Button(actionPanel, text="Save Code", command=self.saveCode, bg="#111111", fg="#00FF00")
        self.autoGenBtn = Button(actionPanel, text="Auto Generate", command=self.autoGenerate, bg="#111111", fg="#00FF00")

        self.ideaBtn.pack(side="left", padx=5, pady=5)
        self.refineBtn.pack(side="left", padx=5, pady=5)
        self.saveBtn.pack(side="left", padx=5, pady=5)
        self.autoGenBtn.pack(padx=5, pady=5)

    def triggerIdeaGeneration(self):
        threading.Thread(target=self.generateIdeaAndCode).start()

    def generateIdeaAndCode(self):
        idea = self.ideaGenerator.generate_idea()
        feedback = self.ceoAdvisor.review_employee("IdeaGenerator", idea, self.code)
        if idea:
            self.queue.put(lambda: self.updateIdeaAndFeedback(idea, feedback))
            code = self.codeGenerator.create_initial_code(idea, feedback)
            self.queue.put(lambda: self.updateCode(code))

    def updateIdeaAndFeedback(self, idea, feedback):
        self.idea = idea
        self.log(f"Idea: {idea}")
        self.ceoFeedback = feedback
        self.log(f"CEO Feedback: {feedback}")
        self.updateUI()

    def updateCode(self, code):
        self.code = code
        self.updateUI()

    def refineCode(self):
        if not self.code.strip():
            messagebox.showinfo("Info", "No code to refine.")
            return
        threading.Thread(target=self.optimizeCode).start()

    def optimizeCode(self):
        feedback = self.feedbackProvider.generate_feedback(self.code)
        optimizedCode = self.codeOptimizer.refine_code(self.code, feedback)
        self.queue.put(lambda: self.updateOptimization(optimizedCode))

    def updateOptimization(self, optimizedCode):
        self.code = optimizedCode if optimizedCode else self.code
        self.executeCode()
        self.updateUI()

    def saveCode(self):
        fileName = self.fileSaver.save_mod_file(self.code)
        messagebox.showinfo("Info", f"Code saved as {fileName}")

    def autoGenerate(self):
        self.generateIdeaAndCode()
        self.refineCode()
        self.log("Auto-generation completed.")

    def updateUI(self):
        self.updateTextArea(self.ideaArea, self.idea, "Idea")
        self.updateTextArea(self.codeArea, self.code, "Code")
        self.updateTextArea(self.feedbackArea, self.feedback, "Feedback")
        self.updateTextArea(self.ceoMessageArea, self.ceoFeedback, "CEO Feedback")
        self.updateTextArea(self.executionResultArea, self.executionOutput, "Execution Result")

    def updateTextArea(self, widget, content, label=None):
        widget.delete('1.0', END)
        widget.insert(END, content)
        if label:
            self.log(f"Updated {label}")

    def log(self, message):
        self.logArea.insert(END, message + "\n")
        self.logArea.see(END)

    def executeCode(self):
        try:
            result = subprocess.run(["python", "-c", self.code], capture_output=True, text=True, timeout=10)
            self.executionOutput = result.stdout if result.stdout else "No output or error occurred."
            self.queue.put(lambda: self.updateExecutionResult(self.executionOutput))
        except subprocess.TimeoutExpired:
            self.executionOutput = "Execution timed out."
        except Exception as e:
            self.executionOutput = str(e)
        finally:
            self.queue.put(lambda: self.updateExecutionResult(self.executionOutput))

    def updateExecutionResult(self, result):
        self.executionOutput = result
        self.updateUI()

    def processQueue(self):
        try:
            while not self.queue.empty():
                task = self.queue.get(0)
                task()
        finally:
            self.master.after(100, self.processQueue)

if __name__ == "__main__":
    root = Tk()
    app = DevEaseApplication(root)
    root.mainloop()
