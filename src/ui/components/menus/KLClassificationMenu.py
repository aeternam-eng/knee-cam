# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk
import shared.constants as constants

# Menu for file operations (opening image files)
class KLClassificationMenu(tk.Menu):
    def __init__(self, master, on_begin_classification) -> tk.Menu:
        super().__init__(master, tearoff=False)
        
        self.add_command(label='Binary Shallow', command=on_begin_classification(constants.ClassifierTypes.BinaryShallow))
        self.add_command(label='Multiclass Shallow', command=on_begin_classification(constants.ClassifierTypes.MulticlassShallow))
        self.add_command(label='Binary CNN', command=on_begin_classification(constants.ClassifierTypes.BinaryCnn))
        self.add_command(label='Multiclass CNN', command=on_begin_classification(constants.ClassifierTypes.MulticlassCnn))
