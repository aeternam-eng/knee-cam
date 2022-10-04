import tkinter as tk
from tkinter import filedialog

# Diálogo para que o usuário escolha um arquivo para leitura
class FileSelectorDialog:
    def __init__(self, on_select):
        root = tk.Tk()
        root.withdraw()

        file_name = filedialog.askopenfilename()

        on_select(file_name)
