import asyncio
import ui.ui as ui

# Ponto de entrada da aplicação, apenas realizando inicializações e chamando o ponto de entrada da interface.
async def main():
    print('Initializing knee-cam...')
    
    asyncio.create_task(ui.render())

if __name__ == "__main__":
    asyncio.run(main())
