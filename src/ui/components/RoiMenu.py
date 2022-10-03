import tkinter as tk

class RoiMenu(tk.Menu):
    def __init__(self, master, on_begin_roi_selection) -> None:
        super().__init__(master, tearoff=False)
        
        self.add_command(label='Select ROI', command=on_begin_roi_selection)
