import flet as ft
import os
import json

def pagina_guias(page: ft.Page):
    ruta_webs = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","storage", "data", "webs.json"))
    with open(ruta_webs, "r", encoding="utf-8") as f:
        data = json.load(f)

    filtro = {"value": ""}

    panels = []

    def build_panels():
        panels.clear()
        filtro_val = filtro["value"].lower()
        for categoria, enlaces in data.items():
            # Filtra las guías por el filtro actual
            guias_filtradas = [
                guia for guia in enlaces
                if filtro_val in guia["titulo"].lower()
            ]
            if not guias_filtradas:
                continue
            panels.append(
                ft.ExpansionPanel(
                    header=ft.ListTile(
                        title=ft.Text(categoria.capitalize(), weight=ft.FontWeight.BOLD)
                    ),
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.TextButton(
                                    text=guia["titulo"],
                                    url=guia["url"],
                                    style=ft.ButtonStyle(color=ft.Colors.BLUE_400),
                                )
                                for guia in guias_filtradas
                            ],
                            spacing=8
                        ),
                        padding=ft.padding.all(16)
                    ),
                    expanded=False
                )
            )

    panel_list = ft.ExpansionPanelList(
        controls=panels,
        expand_icon_color=ft.Colors.BLUE_400,
        elevation=4,
    )

    def on_search(e):
        filtro["value"] = e.control.value
        build_panels()
        panel_list.controls = panels
        panel_list.update()

    # Inicializa los paneles
    build_panels()
    panel_list.controls = panels

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
                content=ft.ListView(
                    expand=True,
                    controls=[panel_list]
                )
            )
        ]
    )