import tkinter as tk

class SaveFileMenu(tk.Menu):
    def __init__(self, master, on_save_image) -> tk.Menu:
        super().__init__(master, tearoff=False)

        self.add_command(label='Save ROI', command=on_save_image)
