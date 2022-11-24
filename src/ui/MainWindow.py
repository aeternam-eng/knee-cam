# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk

from ui.components.ImageViewer import ImageViewer
from ui.components.FileSelectorDialog import FileSelectorDialog
from ui.components.menus.FileMenu import FileMenu
from ui.components.menus.RoiMenu import RoiMenu
from ui.components.menus.KLClassificationMenu import KLClassificationMenu

# Tela principal do aplicativo, sendo o ponto de entrada
class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self._viewer: ImageViewer = None

        self.geometry('800x600')
        self.title('Knee Cam')

        app_menu = tk.Menu(self)
        app_menu.add_cascade(label="File", menu=FileMenu(master=app_menu, on_open_image=lambda: FileSelectorDialog(on_select=self._on_image_selected), on_find_in_image=lambda: FileSelectorDialog(on_select=self._on_find_in_image)))
        app_menu.add_cascade(label="ROI", menu=RoiMenu(master=app_menu, on_begin_roi_selection=lambda: self._viewer.begin_roi_selection() if self._viewer is not None else tk.messagebox.showerror('Error!', "Select an image first")))
        # app_menu.add_cascade(label="Histogram", menu=HistogramMenu(master=app_menu, on_show_histogram=lambda: self._viewer.show_histogram() if self._viewer is not None else tk.messagebox.showerror('Error!', "Select an image first")))
        app_menu.add_cascade(label="KL Classification", menu=KLClassificationMenu(master=app_menu, on_begin_classification=lambda type: self._viewer.begin_classification(type) if self._viewer is not None else tk.messagebox.showerror('Error!', "Select an image first")))

        self.config(menu=app_menu)

    # Ao carregar uma imagem pelo menu de Arquivo para correlacionar duas imagens
    def _on_find_in_image(self, path):
        if(self._viewer is None):
            tk.messagebox.showerror('Error!', "You must have an image open to find another in it")
        else:
            self._viewer.find_inside(path)

    # Ao selecionar uma imagem para abrir e visualizar
    def _on_image_selected(self, path) -> None:
        print(f"opened: {path}")

        if(self._viewer is not None):
            self._viewer.destroy()

        self._viewer = ImageViewer(self, path=path)
