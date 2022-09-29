import dearpygui.dearpygui as dpg

import ui.views.image_viewer as image_viewer

def button_callback():
    print('help')

async def render():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    image_viewer.render();

    with dpg.window(id="main", label="example"):
        dpg.add_text('Hello world')
        dpg.add_button(label="save", callback=button_callback)
        dpg.add_input_text(label='string')
        dpg.add_slider_float(label='float')
        dpg.add_file_dialog(label="help")

    dpg.set_primary_window('main', True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

