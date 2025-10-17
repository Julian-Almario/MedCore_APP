import os
import flet as ft

# Carpeta donde se almacenan los archivos Markdown
RUTA_MDS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "guias"))
os.makedirs(RUTA_MDS, exist_ok=True)

def listar_mds():
    return [f for f in os.listdir(RUTA_MDS) if f.lower().endswith(".md")]

def pantalla_home(page: ft.Page):
    lista_tarjetas = ft.Column(spacing=10, expand=True)
    mostrar_barra = True

    # Layout principal
    layout_principal = ft.Column(expand=True)

    def construir_tarjetas(filtro=""):
        lista_tarjetas.controls.clear()
        archivos = listar_mds()
        filtro = filtro.lower()
        encontrados = False

        if not archivos:
            lista_tarjetas.controls.append(
                ft.Container(
                    content=ft.Text("No tienes archivos Markdown subidos", size=16, color=ft.Colors.RED, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    height=120
                )
            )
        else:
            for archivo in archivos:
                nombre_sin_ext = os.path.splitext(archivo)[0]
                if filtro in nombre_sin_ext.lower():
                    card = ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(
                                        nombre_sin_ext,
                                        size=18,
                                        text_align=ft.TextAlign.CENTER,
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=20,
                            width=True,
                            height=80,
                            alignment=ft.alignment.center,
                            on_click=lambda e, a=archivo: ver_md(a),
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=16),
                        elevation=2,
                    )
                    lista_tarjetas.controls.append(card)
                    encontrados = True
            if not encontrados:
                lista_tarjetas.controls.append(
                    ft.Container(
                        content=ft.Text("No se encontraron resultados.", size=16, color=ft.Colors.OUTLINE, text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        height=120
                    )
                )
        page.update()

    def filtrar_md(e):
        filtro = e.control.value
        construir_tarjetas(filtro)

    def mostrar_lista():
        nonlocal mostrar_barra
        mostrar_barra = True
        construir_tarjetas()
        actualizar_layout()

    def ver_md(nombre_md):
        nonlocal mostrar_barra
        mostrar_barra = False
        ruta_md = os.path.join(RUTA_MDS, nombre_md)
        with open(ruta_md, "r", encoding="utf-8") as f:
            contenido = f.read()
        lista_tarjetas.controls.clear()
        lista_tarjetas.controls.extend([
            ft.Row([
                ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    tooltip="Volver",
                    on_click=lambda e: mostrar_lista()
                ),
                ft.Text(os.path.splitext(nombre_md)[0], size=22),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Container(
                ft.Markdown(
                    contenido,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    expand=True,
                    auto_follow_links=True,
                ),
                expand=True,
                padding=ft.padding.all(30),
            ),
        ])
        actualizar_layout()

    # Buscador de perlas
    search_bar = ft.TextField(
        label="Buscar pearls...",
        on_change=filtrar_md,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.Colors.OUTLINE,
        bgcolor=ft.Colors.TRANSPARENT,
        filled=False,
        dense=True,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        width=400,
        expand=True,
    )

    # Barra fiaja superior
    barra_superior = ft.Container(
        content=ft.Row(
            controls=[search_bar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=10),
        alignment=ft.alignment.center,
    )

    area_scroll = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[lista_tarjetas],
            expand=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        ),
    )

    def actualizar_layout():
        layout_principal.controls.clear()
        if mostrar_barra:
            layout_principal.controls.extend([
                barra_superior,
                area_scroll
            ])
        else:
            layout_principal.controls.extend([
                area_scroll
            ])
        page.update()

    mostrar_lista()

    return layout_principal