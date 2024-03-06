import threading
from tkinter import Tk
from application import Application

def run_gui():
    root = Tk()
    root.anchor = "center"
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()

def main():
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()
    gui_thread.join()

if __name__ == "__main__":
    main()