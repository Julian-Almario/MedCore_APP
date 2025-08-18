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
    #SCROLL PERSONALIZATION
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
# -------------------------------------------------------------------------------
# Search bar general
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

# -------------------------------------------------------------------------------
# Pagina de medicamentos
    #Ruta de medicamentos
    RUTA_MEDS = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage", "data", "meds"))
    os.makedirs(RUTA_MEDS, exist_ok=True) #Confirmacion de que existe el .json

    #Generacion de panel por cada item de la Base de datos .json
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

        #Datos que se extrain y se muestran del .json
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

# Pagian de algoritmos
    #Ruta de almacenamiento de algoritmos
    RUTA_ALGO = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage", "data", "algoritmos"))
    os.makedirs(RUTA_ALGO, exist_ok=True) #Confirmacion de que exista el .json

    #Extensiones de imagenes validas
    EXTENSIONES_VALIDAS = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"]

    def es_imagen_valida(ruta_imagen):
        return os.path.exists(ruta_imagen) and os.path.splitext(ruta_imagen)[1].lower() in EXTENSIONES_VALIDAS

    def cargar_algoritmos_desde_json(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return [crear_panel_algoritmo(algo) for algo in datos]

    def crear_panel_algoritmo(algo: dict):
        panel_ref = ft.Ref[ft.ExpansionPanel]()

        def on_expand_change(e):
            panel = panel_ref.current
            is_expanded = panel.expanded
            panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
            panel.update()

        ruta_imagen = os.path.join(RUTA_ALGO, algo["imagen"])

        if not es_imagen_valida(ruta_imagen):
            imagen_componente = ft.Text(
                f"Imagen no encontrada o formato no soportado: {algo['imagen']}",
                color=ft.Colors.RED,
                selectable=True
            )
        else:
            imagen_componente = ft.InteractiveViewer(
                min_scale=0.5,
                max_scale=5,
                boundary_margin=ft.margin.all(20),
                content=ft.Image(
                    src=ruta_imagen,
                    fit=ft.ImageFit.CONTAIN,
                    width=600,
                    height=400,
                    expand=True
                )
            )

        #INformacion presentada en las pestañas de la lista
        return {
            "titulo": algo["nombre"],
            "tags": algo["tags"],
            "componente": ft.ExpansionPanelList(
                on_change=on_expand_change,
                expand_icon_color=TEXT_COLOR,
                elevation=8,
                divider_color=TEXT_COLOR,
                controls=[
                    ft.ExpansionPanel(
                        ref=panel_ref,
                        header=ft.ListTile(
                            title=ft.Text(algo["nombre"], text_align=ft.TextAlign.LEFT),
                        ),
                        content=ft.Container(
                            content=imagen_componente,
                            padding=15,
                        ),
                        bgcolor=PRIMARY_COLOR,
                        expanded=False,
                    )
                ],
            )
        }

    #Paginacion global de los algoritmos
    def pagina_algoritmos(page: ft.Page):
        list_data = cargar_algoritmos_desde_json(os.path.join(RUTA_ALGO, "algoritmos.json"))
        buscar = "Buscar algoritmos..."

        mensaje_no_resultados = ft.Text(
            value="No se encontraron algoritmos.",
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

#-------------------------------------------
#Contenido disponible
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
    
    def show_algorithms():
        main_content.controls.clear()
        main_content.controls.append(pagina_algoritmos(page))
        page.update()

    def show_info():
        main_content.controls.clear()
        main_content.controls.append(info_page(page))
        page.update()

#Barra de navegacion personalizada
    def cambiar_pagina(index):
        nonlocal current_page_index
        current_page_index = index
        load_current_page()
        navigation_container.content = custom_navigation_bar()
        page.update()

    def custom_navigation_bar():
        return ft.Row(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            spacing=10,
            controls=[
                #Botones de la barra de navegacion (para crear mas no se te olvide especificar y/o cambia la pagina a la cual apunta)
                ft.TextButton(
                    text="Calculadoras",
                    icon=ft.Icons.CALCULATE_OUTLINED,
                    style=ft.ButtonStyle(color=TEXT_COLOR if current_page_index == 0 else SELECT_COLOR),
                    on_click=lambda e: cambiar_pagina(0),
                ),
                ft.TextButton(
                    text="Medicamentos",
                    icon=ft.Icons.LOCAL_PHARMACY_OUTLINED,
                    style=ft.ButtonStyle(color=TEXT_COLOR if current_page_index == 1 else SELECT_COLOR),
                    on_click=lambda e: cambiar_pagina(1),
                ),
                ft.TextButton(
                    text="Laboratorios",
                    icon=ft.Icons.BIOTECH_OUTLINED,
                    style=ft.ButtonStyle(color=TEXT_COLOR if current_page_index == 2 else SELECT_COLOR),
                    on_click=lambda e: cambiar_pagina(2),
                ),
                ft.TextButton(
                    text="Algoritmos",
                    icon=ft.Icons.DEVICE_HUB_OUTLINED,
                    style=ft.ButtonStyle(color=TEXT_COLOR if current_page_index == 3 else SELECT_COLOR),
                    on_click=lambda e: cambiar_pagina(3),
                ),
                ft.TextButton(
                    text="Historias Clínicas",
                    icon=ft.Icons.DESCRIPTION_OUTLINED,
                    style=ft.ButtonStyle(color=TEXT_COLOR if current_page_index == 4 else SELECT_COLOR),
                    on_click=lambda e: cambiar_pagina(4),
                ),
                ft.TextButton(
                    text="Info",
                    icon=ft.Icons.INFO_OUTLINED,
                    style=ft.ButtonStyle(color=TEXT_COLOR if current_page_index == 5 else SELECT_COLOR),
                    on_click=lambda e: cambiar_pagina(5),
                )

            ]
        )

#Navegacion superior
    navigation_container = ft.Container(
        expand=False,
        width=page.width,
        padding=ft.padding.only(top=8, bottom=8),
        content=ft.Row(
            controls=[custom_navigation_bar()],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

#Paginacion de cada pestaña
    def load_current_page():
        if current_page_index == 0:
            show_cals()
        elif current_page_index == 1:
            show_meds()
        elif current_page_index == 2:
            show_labs()
        elif current_page_index == 3:
            show_algorithms()
        elif current_page_index == 4:
            show_hc()
        elif current_page_index == 5:
            show_info()




    load_current_page()

    page.add(
        ft.Column(
            expand=True,
            controls=[
                main_content,
                navigation_container
            ]
        )
    )

ft.app(target=main, assets_dir="assets")