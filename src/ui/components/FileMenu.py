import tkinter as tk

class FileMenu(tk.Menu):
    def __init__(self, master, on_open_image, on_find_in_image) -> tk.Menu:
        super().__init__(master, tearoff=False)
        
        self.add_command(label='Open Image', command=on_open_image)
        self.add_command(label='Find in opened image...', command=on_find_in_image)
