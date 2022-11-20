# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk

# Menu for file operations (opening image files)
class FileMenu(tk.Menu):
    def __init__(self, master, on_open_image, on_find_in_image) -> tk.Menu:
        super().__init__(master, tearoff=False)
        
        self.add_command(label='Open Image', command=on_open_image)
        self.add_command(label='Find in opened image...', command=on_find_in_image)
