import tkinter as tk
from tkinter import filedialog

class FileSelectorDialog:
    def __init__(self, on_select):
        root = tk.Tk()
        root.withdraw()

        file_name = filedialog.askopenfilename()

        on_select(file_name)
