import threading
from tkinter import Tk
from application import Application

def main():
    root = Tk()
    root.anchor = "center"
    app = Application(root)

    # Run the GUI event loop in the main thread
    root.mainloop()

if __name__ == "__main__":
    main()