import os
import flet as ft

# Carpeta donde se almacenan los archivos Markdown
RUTA_MDS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "guias"))
os.makedirs(RUTA_MDS, exist_ok=True)

def listar_mds():
    return [f for f in os.listdir(RUTA_MDS) if f.lower().endswith(".md")]

def pantalla_home(page: ft.Page):
    # Column principal con scroll en el borde de la pantalla
    contenido_principal = ft.Column(
        controls=[],  # Se llenará dinámicamente
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    lista_tarjetas = ft.Column(spacing=10, expand=True)

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
                    height=120  # Altura mínima para mantener el layout
                )
            )
        else:
            for archivo in archivos:
                nombre_sin_ext = os.path.splitext(archivo)[0]
                if filtro in nombre_sin_ext.lower():
                    card = ft.Card(
                        content=ft.Container(
                            content=ft.Text(
                                nombre_sin_ext,
                                size=18,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            padding=20,  # Más espacio interno
                            width=350,   # Ajusta el ancho del card
                            height=80,   # Ajusta el alto del card
                            alignment=ft.alignment.center,  # Centra el contenido dentro del container
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
                        height=120  # Altura mínima para mantener el layout
                    )
                )
        page.update()

    def filtrar_md(e):
        filtro = e.control.value
        construir_tarjetas(filtro)

    def mostrar_lista():
        contenido_principal.controls.clear()

        search_bar = ft.TextField(
            label="Buscar pearls...",
            on_change=filtrar_md,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.OUTLINE,
            bgcolor=ft.Colors.TRANSPARENT,
            filled=False,
            dense=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
            width=300,
        )

        construir_tarjetas()

        barra_superior = ft.Row(
            controls=[
                ft.Container(content=search_bar),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        contenido_principal.controls.extend([
            barra_superior,
            lista_tarjetas
        ])
        page.update()

    def ver_md(nombre_md):
        ruta_md = os.path.join(RUTA_MDS, nombre_md)
        with open(ruta_md, "r", encoding="utf-8") as f:
            contenido = f.read()
        contenido_principal.controls.clear()
        contenido_principal.controls.extend([
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
                padding=ft.padding.all(30),  # Espaciado de 20px en todos los bordes
            ),
        ])
        page.update()

    mostrar_lista()
    return contenido_principal