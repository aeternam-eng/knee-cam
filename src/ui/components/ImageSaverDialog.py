# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Dialógo para que o usuário diga o nome de salvamento de um arquivo de imagem.
class ImageSaverDialog:
    def __init__(self, image):
        root = tk.Tk()
        root.withdraw()

        file_name = filedialog.asksaveasfilename(defaultextension='.png')

        if file_name:
            image.save(file_name)
        else:
            messagebox.showwarning('No name provided for the image')
