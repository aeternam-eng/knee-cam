# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk

# Menu com opções para iniciar a seleção de um ROI na tela principal
class RoiMenu(tk.Menu):
    def __init__(self, master, on_begin_roi_selection) -> None:
        super().__init__(master, tearoff=False)
        
        self.add_command(label='Select ROI', command=on_begin_roi_selection)
