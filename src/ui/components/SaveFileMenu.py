import tkinter as tk

# Menu da tela de visualização de ROI para salvar a ROI selecionada
class SaveFileMenu(tk.Menu):
    def __init__(self, master, on_save_image) -> tk.Menu:
        super().__init__(master, tearoff=False)

        self.add_command(label='Save ROI', command=on_save_image)
