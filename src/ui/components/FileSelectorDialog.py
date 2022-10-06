# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk
from tkinter import filedialog

# Diálogo para que o usuário escolha um arquivo para leitura
class FileSelectorDialog:
    def __init__(self, on_select):
        root = tk.Tk()
        root.withdraw()

        file_name = filedialog.askopenfilename()

        on_select(file_name)
