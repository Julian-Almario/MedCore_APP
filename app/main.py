import flet as ft
from modules.home import *
from modules.cal import *
from modules.nav import *
from modules.info import *
from modules.hc import *
from modules.labs import *


def main(page: ft.Page):
    page.title = "MedCore"
    page.theme_mode = ft.ThemeMode.DARK
    page.adaptive = True

    # Pagination
    current_page_index = 0

    def on_navigation_change(e):
        nonlocal current_page_index
        current_page_index = e.control.selected_index
        load_current_page()
        page.close(drawer)
        page.update()

    # Navigation interface
    bar, drawer = nav(page, on_navigation_change)

    # Pages add 
    def show_home():
        page.controls.clear()
        page.add(bar,pantalla_home(page))
        page.update()

    def show_meds():
        page.controls.clear()
        page.add(bar, ft.Text("Medicamentos"))
        page.update()
    
    def show_cals():
        page.controls.clear()
        page.add(bar, list_content_search(calculadoras))
        page.update()

    def show_labs():
        page.controls.clear()
        page.add(bar, list_content_search(paraclinicos))
        page.update()

    def show_hc():
        page.controls.clear()
        page.add(bar, pantalla_historia_clinica(page))
        page.update()

    def show_info():
        page.controls.clear()
        page.add(bar, info_page())
        page.update()

    def load_current_page():
        if current_page_index == 0:
            show_home()
        elif current_page_index == 1:
            show_meds()
        elif current_page_index == 2:
            show_cals()
        elif current_page_index == 3:
            show_labs()
        elif current_page_index == 4:
            show_hc()
        elif current_page_index == 5:
            show_info()

    # Init page
    show_home()

ft.app(main)