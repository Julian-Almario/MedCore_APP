import flet as ft
import os
import json
from modules.colors import *

def pagina_guias(page: ft.Page):
    ruta_webs = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "webs.json"))
    with open(ruta_webs, "r", encoding="utf-8") as f:
        data = json.load(f)

    filtro = {"value": ""}
    lista_paneles = []

    def crear_panel_categoria(categoria, guias):
        panel_ref = ft.Ref[ft.ExpansionPanel]()

        contenido = ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center_left,
                    content=ft.TextButton(
                        text=guia["titulo"],
                        url=guia["url"],
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_400,
                            overlay_color=ft.Colors.BLUE_100,
                            padding=ft.padding.symmetric(horizontal=8, vertical=6),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    )
                )
                for guia in guias
            ],
            spacing=10
        )


        return ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    ref=panel_ref,
                    header=ft.ListTile(
                        title=ft.Text(categoria.capitalize()),
                    ),
                    content=ft.Container(content=contenido, padding=15),
                    bgcolor=PRIMARY_COLOR,
                    expanded=False
                )
            ],
            expand_icon_color=TEXT_COLOR,
            elevation=8,
            divider_color=TEXT_COLOR,
        )

    def build_panels():
        lista_paneles.clear()
        filtro_val = filtro["value"].lower()

        for categoria, enlaces in data.items():
            guias_filtradas = [
                guia for guia in enlaces
                if filtro_val in guia["titulo"].lower()
            ]
            if not guias_filtradas:
                continue

            panel = crear_panel_categoria(categoria, guias_filtradas)
            lista_paneles.append(
                ft.Container(
                    content=panel,
                    margin=ft.margin.only(bottom=16)
                )
            )

    def on_search(e):
        filtro["value"] = e.control.value
        build_panels()
        lista_view.controls = lista_paneles
        lista_view.update()

    build_panels()

    lista_view = ft.ListView(
        expand=True,
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        controls=lista_paneles
    )

    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                content=ft.TextField(
                    label="Buscar guía...",
                    on_change=on_search,
                    border=ft.InputBorder.UNDERLINE,
                    border_color=ft.Colors.OUTLINE,
                    bgcolor=ft.Colors.TRANSPARENT,
                    filled=False,
                    dense=True,
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
                    width=400,
                    expand=True,
                ),
                padding=ft.padding.symmetric(horizontal=40, vertical=10),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                expand=True,
                content=lista_view
            )
        ]
    )
