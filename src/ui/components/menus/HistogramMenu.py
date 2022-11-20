# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk

# Menu for file operations (opening image files)
class HistogramMenu(tk.Menu):
    def __init__(self, master, on_show_histogram) -> tk.Menu:
        super().__init__(master, tearoff=False)
        
        self.add_command(label='Show Histogram', command=on_show_histogram)
