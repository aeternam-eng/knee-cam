import asyncio
from ui.MainWindow import MainWindow;

# Ponto de entrada da aplicação, apenas realizando inicializações e chamando o ponto de entrada da interface.
def main():
    print('Initializing knee-cam...')

    gui = MainWindow()

    gui.protocol("WM_DELETE_WINDOW", gui.destroy)
    gui.mainloop()

if __name__ == "__main__":
    main()
