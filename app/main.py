import flet as ft
import os
import json
from modules.cal import *
from modules.info import *
from modules.hc import *
from modules.labs import *


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.adaptive = True
    page.title = "MedCore"
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=0,
            radius=0,
            thumb_color=ft.Colors.TRANSPARENT,
            track_color=ft.Colors.TRANSPARENT,
            track_border_color=ft.Colors.TRANSPARENT,
        )
    )

    current_page_index = 0
    main_content = ft.Column(expand=True)

    def search_bar(filtrar, buscar):
        return ft.TextField(
            label=buscar,
            on_change=filtrar,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.OUTLINE,
            bgcolor=ft.Colors.TRANSPARENT,
            filled=False,
            dense=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            width=400,
            expand=True,
        )

    def list_content_search(list_content, mensaje_no_resultados):
        list_content.sort(key=lambda x: x["titulo"].lower())
        list_container = ft.Column(spacing=20)

        def build_list(filtered_items):
            list_container.controls.clear()
            if filtered_items:
                for cont in filtered_items:
                    list_container.controls.append(cont["componente"])
            else:
                list_container.controls.append(
                    ft.Container(
                        content=mensaje_no_resultados,
                        alignment=ft.alignment.center,
                        padding=50,
                    )
                )
            list_container.update()

        def filtrar_items(e):
            filtro = e.control.value.lower()
            filtered_items = []
            for cont in list_content:
                titulo = cont["titulo"].lower()
                tags = " ".join(cont["tags"]).lower()
                if filtro in titulo or filtro in tags:
                    filtered_items.append(cont)
            build_list(filtered_items)

        for cont in list_content:
            list_container.controls.append(cont["componente"])

        return list_container, filtrar_items

    def build_fixed_page(list_data, placeholder_busqueda):
        mensaje_no_resultados = ft.Text(
            value="No se encontraron resultados",
            style=ft.TextThemeStyle.BODY_MEDIUM,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        list_container, filtrar_items = list_content_search(list_data, mensaje_no_resultados)

        return ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    content=search_bar(filtrar_items, placeholder_busqueda),
                    padding=ft.padding.symmetric(horizontal=40, vertical=10),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        controls=[list_container],
                    ),
                ),
            ],
        )

    
#----------------------------------------------
    #Page meds

    RUTA_MEDS = os.path.abspath(os.path.join(os.path.dirname(__file__),"storage", "data"))
    os.makedirs(RUTA_MEDS, exist_ok=True)

    def crear_panel_medicamento(med: dict):
        panel_ref = ft.Ref[ft.ExpansionPanel]()

        def fila_info(titulo: str, contenido: str):
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                        width=150,
                        padding=ft.padding.symmetric(vertical=6),
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=ft.Text(contenido, size=14, color=ft.Colors.ON_SURFACE),
                        padding=ft.padding.symmetric(vertical=6),
                        alignment=ft.alignment.center_left,
                        expand=True
                    )
                ],
                spacing=10
            )

        contenido_panel = ft.Column(
            controls=[
                fila_info("Mecanismo de acción:", med["mecanismo"]),
                fila_info("Indicaciones:", med["indicaciones"]),
                fila_info("Dosis:", med["dosis"]),
                fila_info("Contraindicaciones:", med["contraindicaciones"]),
                fila_info("Observaciones:", med["observaciones"])
            ],
            spacing=0
        )

        def on_expand_change(e):
            panel = panel_ref.current
            is_expanded = panel.expanded
            panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
            panel.update()

        return {
            "titulo": med["nombre"],
            "tags": med["tags"],
            "componente": ft.ExpansionPanelList(
                on_change=on_expand_change,
                expand_icon_color=TEXT_COLOR,
                elevation=8,
                divider_color=TEXT_COLOR,
                controls=[
                    ft.ExpansionPanel(
                        ref=panel_ref,
                        header=ft.ListTile(
                            title=ft.Text(med["nombre"], text_align=ft.TextAlign.LEFT),
                        ),
                        content=ft.Container(
                            content=contenido_panel,
                            padding=15
                        ),
                        bgcolor=PRIMARY_COLOR,
                        expanded=False
                    )
                ],
            )
        }
    
    #Database load meds.json
    def cargar_medicamentos_desde_json(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        return [crear_panel_medicamento(med) for med in datos]


    def pagina_medicamentos(page: ft.Page):

        list_data = cargar_medicamentos_desde_json(f"{RUTA_MEDS}/meds.json")

        buscar = "Buscar medicamentos..."
        mensaje_no_resultados = ft.Text(
            value="No se encontraron medicamentos.",
            style=ft.TextThemeStyle.BODY_MEDIUM,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        list_container, filtrar_items = list_content_search(list_data, mensaje_no_resultados)

        return ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    content=search_bar(filtrar_items, buscar),
                    padding=ft.padding.symmetric(horizontal=40, vertical=10),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        controls=[list_container],
                    ),
                ),
            ],
        )



#--------------------------------------------------

    def show_cals():
        main_content.controls.clear()
        main_content.controls.append(build_fixed_page(calculadoras, "Buscar calculadora..."))
        page.update()

    def show_meds():
        main_content.controls.clear()
        main_content.controls.append(pagina_medicamentos(page))
        page.update()

    def show_labs():
        main_content.controls.clear()
        main_content.controls.append(build_fixed_page(paraclinicos, "Buscar laboratorio..."))
        page.update()

    def show_hc():
        main_content.controls.clear()
        main_content.controls.append(pantalla_historia_clinica(page))
        page.update()

    def show_info():
        main_content.controls.clear()
        main_content.controls.append(info_page(page))
        page.update()

    def on_navigation_change(e):
        nonlocal current_page_index
        current_page_index = e.control.selected_index
        load_current_page()

    # Load pages

    def load_current_page():
        if current_page_index == 0:
            show_cals()
        #Page meds in progress
        #elif current_page_index == 1:
        #    show_meds()
        elif current_page_index == 1:
            show_labs()
        elif current_page_index == 2:
            show_hc()
        elif current_page_index == 3:
            show_info()

    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=PRIMARY_COLOR,
        inactive_color=SELECT_COLOR,
        active_color=TEXT_COLOR,
        on_change=on_navigation_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CALCULATE_OUTLINED, label="Calculadoras"),
            #ft.NavigationBarDestination(icon=ft.Icons.LOCAL_PHARMACY_OUTLINED, label="Medicamentos"),
            ft.NavigationBarDestination(icon=ft.Icons.BIOTECH_OUTLINED, label="Laboratorios"),
            ft.NavigationBarDestination(icon=ft.Icons.DESCRIPTION_OUTLINED, label="Historia"),
            ft.NavigationBarDestination(icon=ft.Icons.INFO_OUTLINED, label="Info"),
        ],
    )

    load_current_page()
    page.add(main_content)

ft.app(target=main, assets_dir="assets")