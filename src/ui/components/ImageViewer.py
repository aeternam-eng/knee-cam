# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import operator
import tkinter as tk
import cv2 as cv
import numpy as np
from PIL import Image, ImageTk

from ui.components.RoiViewer import RoiViewer
from ui.components.SelectableCanvas import SelectableCanvas

# Carrega, e exibe a imagem
class ImageViewer(tk.Frame):
    def __init__(self, master, path):
        super().__init__(master)

        self._loaded_image = Image.open(path)

        self._image_canvas = SelectableCanvas(master=self, on_select=self._on_selection_done)
        self._image_canvas.config(scrollregion=(0, 0, self._loaded_image.size[0], self._loaded_image.size[1]))

        horizontal_scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._image_canvas.xview)
        vertical_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._image_canvas.yview)

        self._image_canvas.config(xscrollcommand=horizontal_scrollbar.set)
        self._image_canvas.config(yscrollcommand=vertical_scrollbar.set)

        # Imagens precisam ser referênciadas pela instância para que o garbage collector não limpe (??????)
        self._render = ImageTk.PhotoImage(self._loaded_image)

        self._image_canvas.create_image(0, 0, anchor='nw', image=self._render)

        horizontal_scrollbar.pack(fill=tk.X, side=tk.BOTTOM)
        vertical_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self._image_canvas.pack(fill=tk.BOTH, expand=True)
        self.pack(fill=tk.BOTH, expand=True)

    # Callback do Canvas ao finalizar uma seleção, exibindo o ROI selecionado
    def _on_selection_done(self, start_point, end_point):
        crop_coordinates = (start_point[0], start_point[1], end_point[0], end_point[1])
        sliced_image = self._loaded_image.crop(crop_coordinates)

        self._roi_viewer = RoiViewer(self.master, image=sliced_image)
        self._roi_viewer.protocol("WM_DELETE_WINDOW", self._roi_viewer.destroy)

    # Interface que permite classes externas iniciarem uma correlação com outra imagem
    # Exibe um retângulo com o padrão encontrado
    def find_inside(self, path):
        comparison_method = cv.TM_CCORR_NORMED

        template = cv.imread(path, cv.IMREAD_GRAYSCALE)
        main_as_opencv = cv.cvtColor(np.asarray(self._loaded_image), cv.COLOR_BGR2GRAY)

        matches = cv.matchTemplate(main_as_opencv, template, comparison_method)
        _, _, _, local_maximum = cv.minMaxLoc(matches)

        template_dimensions = (template.shape[1], template.shape[0])

        top_left = local_maximum
        bottom_right = tuple(map(operator.add, top_left, template_dimensions))

        self._image_canvas.create_rectangle(top_left[0], top_left[1], bottom_right[0], bottom_right[1], outline='red')

    # Interface que permite classes externas iniciarem uma seleção de ROI
    def begin_roi_selection(self):
        self._image_canvas.begin_selection()
