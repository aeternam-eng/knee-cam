# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

from ui.MainWindow import MainWindow

# Ponto de entrada da aplicação, apenas realizando inicializações e chamando o ponto de entrada da UI.
def main():
    print('Initializing knee-cam...')

    gui = MainWindow()

    gui.protocol("WM_DELETE_WINDOW", gui.destroy)
    gui.mainloop()

if __name__ == "__main__":
    main()
