# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import tkinter as tk

# Exibe uma imagem mas com a funcionalidade de desenhar uma Região de Interesse (ROI)
class SelectableCanvas(tk.Canvas):
    def __init__(self, master, on_select):
        super().__init__(master, cursor='left_ptr')

        self._on_select = on_select
        self._startPoint = None
        self._endPoint = None
        self._selection = None

    # Realiza a limpeza necessária ao desativar/finalizar o modo de seleção
    def _cleanup(self):
        self.bind("<ButtonPress-1>", lambda e: None)
        self.bind("<B1-Motion>", lambda e: None)
        self.bind("<ButtonRelease-1>", lambda e: None)

        self._startPoint = None
        self._endPoint = None
        self.delete(self._selection)
        self.config(cursor='left_ptr')

    # Converte as coordenadas de um evento para coordenadas locais do Canvas
    def _get_canvas_coordinates(self, event):
        return tuple((self.canvasx(event.x), self.canvasy(event.y)))

    def _on_mouse_press(self, event):
        self._startPoint = self._get_canvas_coordinates(event)

        if(not self._selection):
            self._selection = self.create_rectangle(0, 0, 1, 1, outline='red')

    # Atualiza a exibição do retângulo ao mover o mouse
    def _on_mouse_move(self, event):
        current_coordinates = self._get_canvas_coordinates(event)
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()

        if event.x > 0.9 * canvas_width:
            self.xview_scroll(1, 'units')
        elif event.x < 0.1 * canvas_width:
            self.xview_scroll(-1, 'units')

        if event.y > 0.9 * canvas_height:
            self.yview_scroll(1, 'units')
        elif event.y < 0.1 * canvas_height:
            self.yview_scroll(-1, 'units')

        self._endPoint = current_coordinates
        self.coords(self._selection, self._startPoint[0], self._startPoint[1], self._endPoint[0], self._endPoint[1])

    # Confirmação de que o retângulo foi selecionado ao soltar o mouse
    def _on_mouse_release(self, event):
        self._endPoint = self._get_canvas_coordinates(event)

        if(self._selection):
            self._on_select(self._startPoint, self._endPoint)
        
        self._cleanup()

    # Permite a classes externas que iniciem uma seleção de ROI
    def begin_selection(self):
        self.bind("<ButtonPress-1>", self._on_mouse_press)
        self.bind("<B1-Motion>", self._on_mouse_move)
        self.bind("<ButtonRelease-1>", self._on_mouse_release)

        self.config(cursor='crosshair')
