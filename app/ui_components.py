import threading
from tkinter import Button, Frame, Label, Scrollbar, Text, PhotoImage, END, VERTICAL

class UIComponents:
    def __init__(self, master, application):
        self.master = master
        self.application = application
        self.setup_background()
        self.setup_log()
        self.setup_buttons()
        self.setup_text_areas()

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

        self.generate_idea_button = Button(button_frame, text="Generate Idea", command=self.generate_idea_thread, bg="#111111", fg="#00FF00")
        self.refine_code_button = Button(button_frame, text="Refine Code", command=self.refine_code_thread, bg="#111111", fg="#00FF00")
        self.save_final_code_button = Button(button_frame, text="Save Code", command=self.save_final_code_thread, bg="#111111", fg="#00FF00")
        self.auto_generate_button = Button(button_frame, text="Auto Generate", command=self.auto_generate_thread, bg="#111111", fg="#00FF00")

        self.generate_idea_button.pack(side="left", padx=5, pady=5)
        self.refine_code_button.pack(side="left", padx=5, pady=5)
        self.save_final_code_button.pack(side="left", padx=5, pady=5)
        self.auto_generate_button.pack(side="left", padx=5, pady=5)

        self.buttons = [
            self.generate_idea_button,
            self.refine_code_button,
            self.save_final_code_button,
            self.auto_generate_button
        ]

    def setup_text_areas(self):
        self.idea_text, self.idea_scrollbar = self.create_text_area("Current Idea", 0, 0)
        self.code_text, self.code_scrollbar = self.create_text_area("Current Code", 0, 1)
        self.feedback_text, self.feedback_scrollbar = self.create_text_area("Current Feedback", 1, 0)
        self.ceo_message_text, self.ceo_message_scrollbar = self.create_text_area("CEO Message", 1, 1)
        self.code_output_text, self.code_output_scrollbar = self.create_text_area("Code Execution Result", 2, 0)

    def create_text_area(self, label_text, row, column):
        frame = Frame(self.master, background="black", borderwidth=1, relief="solid")
        label = Label(frame, text=label_text, fg="#00FF00", bg="black")
        label.pack(side="top", fill="x")
        text_widget = Text(frame, height=10, width=40, wrap="word", bg="#111111", fg="#00FF00", insertbackground="#00FF00",
                           borderwidth=0, highlightthickness=0)
        scrollbar = Scrollbar(frame, command=text_widget.yview, orient=VERTICAL)
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")
        return text_widget, scrollbar

    def log_message(self, message):
        self.log.insert(END, message + "\n")
        self.log.see(END)

    def update_text_area(self, text_widget, content):
        text_widget.delete('1.0', END)
        if content:
            if isinstance(content, str):
                text_widget.insert(END, content)
            else:
                text_widget.insert(END, str(content))

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state="disabled")

    def enable_buttons(self):
        for button in self.buttons:
            button.config(state="normal")

    def generate_idea_thread(self):
        threading.Thread(target=self.application.generate_idea).start()

    def refine_code_thread(self):
        threading.Thread(target=self.application.refine_code).start()

    def save_final_code_thread(self):
        threading.Thread(target=self.application.save_final_code).start()

    def auto_generate_thread(self):
        threading.Thread(target=self.application.auto_generate).start()