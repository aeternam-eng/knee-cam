import tkinter as tk
from PIL import ImageTk

from ui.components.ImageSaverDialog import ImageSaverDialog
from ui.components.SaveFileMenu import SaveFileMenu

class RoiViewer(tk.Toplevel):
    def __init__(self, master, image):
        super().__init__(master)

        self._image = image
        self._rendered_image = ImageTk.PhotoImage(self._image)

        self._image_container = tk.Label(self, image=self._rendered_image)
        self._image_container.place(x=0, y=0)

        image_width, image_height = image.size
        dimensions = f"{image_width}x{image_height}"

        save_menu = SaveFileMenu(self, on_save_image=lambda: ImageSaverDialog(self._image))

        self.config(menu=save_menu)
        self.title(f"ROI ({dimensions})")
        self.geometry(dimensions)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
