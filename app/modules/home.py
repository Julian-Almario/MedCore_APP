import os
import flet as ft
import requests  # Agrega esta importación

# Carpeta donde se almacenan los archivos Markdown
RUTA_MDS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "guias"))
os.makedirs(RUTA_MDS, exist_ok=True)

BACKEND_URL = "http://localhost:8000"  # backend URL

def listar_mds():
    return [f for f in os.listdir(RUTA_MDS) if f.lower().endswith(".md")]

def pantalla_home(page: ft.Page):
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

    def descargar_md_desde_backend(e):
        try:
            resp = requests.get(f"{BACKEND_URL}/pearls")
            resp.raise_for_status()
            archivos = resp.json().get("pearls", [])
            descargados = 0

            for archivo in archivos:
                archivo_url = f"{BACKEND_URL}/pearls/{archivo}"
                r = requests.get(archivo_url)
                if r.status_code == 200:
                    with open(os.path.join(RUTA_MDS, archivo), "w", encoding="utf-8") as f:
                        f.write(r.text)
                    descargados += 1

            # Crear un diálogo de éxito
            dlg_exito = ft.AlertDialog(
                title=ft.Text("Descarga completada"),
                content=ft.Text(f"Se Actualizacon las guias"),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_exito))
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dlg_exito
            page.open(dlg_exito)

            construir_tarjetas()

        except Exception as ex:
            # Crear un diálogo de error
            dlg_error = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Ocurrió un error al descargar los archivos."),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_error))
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dlg_error
            page.open(dlg_error)



    def mostrar_lista():
        construir_tarjetas()
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

    # Barra superior: search bar y botón
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

    btn_descargar = ft.ElevatedButton(
        text="Actualizar perlas",
        icon=ft.Icons.DOWNLOAD,
        on_click=descargar_md_desde_backend,
        style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=20, vertical=10)),
    )

    barra_superior = ft.Container(
        content=ft.Row(
            controls=[search_bar, btn_descargar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=10),
        alignment=ft.alignment.center,
    )

    # Área con scroll solo para las tarjetas
    area_scroll = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[lista_tarjetas],
            expand=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        ),
    )

    mostrar_lista()

    return ft.Column(
        expand=True,
        controls=[
            barra_superior,
            area_scroll
        ]
    )