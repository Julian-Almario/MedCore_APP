import os
import flet as ft

# Carpeta donde se almacenan los archivos Markdown
RUTA_MDS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "guias"))
RUTA_NOTAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "notas"))
os.makedirs(RUTA_MDS, exist_ok=True)
os.makedirs(RUTA_NOTAS, exist_ok=True)

def listar_mds():
    return [f for f in os.listdir(RUTA_MDS) if f.lower().endswith(".md")]

def listar_notas():
    return [f for f in os.listdir(RUTA_NOTAS) if f.lower().endswith(".md")]

def pantalla_home(page: ft.Page):
    lista_tarjetas = ft.Column(spacing=10, expand=True)
    lista_notas = ft.Column(spacing=10, expand=True)
    mostrar_barra = True
    current_view = "tabs"

    # Layout principal
    layout_principal = ft.Column(expand=True)

    # --- Perlas ---
    def construir_tarjetas(filtro=""):
        lista_tarjetas.controls.clear()
        archivos = listar_mds()
        filtro = (filtro or "").lower()
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
            for archivo in sorted(archivos, key=lambda x: x.lower()):
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

    def filtrar_md(e):
        # mantenemos por compatibilidad pero no dependemos del evento
        filtro = (search_bar.value or "").strip()
        construir_tarjetas(filtro)

    def filtrar_notas(e):
        filtro = (search_bar.value or "").strip()
        construir_notas(filtro)

    # Filtrar leyendo directamente el valor actual del search_bar y la pestaña activa
    def filter_current_value(_e=None):
        try:
            idx = tabs.selected_index
        except Exception:
            idx = 0
        valor = (search_bar.value or "").strip()
        if idx == 0:
            construir_tarjetas(valor)
        else:
            construir_notas(valor)
        page.update()

    def mostrar_lista():
        nonlocal mostrar_barra, current_view
        mostrar_barra = True
        current_view = "tabs"
        construir_tarjetas()
        construir_notas()  # mantener notas actualizadas
        actualizar_layout()

    def ver_md(nombre_md):
        nonlocal mostrar_barra, current_view
        mostrar_barra = False
        current_view = "perla"
        ruta_md = os.path.join(RUTA_MDS, nombre_md)
        try:
            with open(ruta_md, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception:
            contenido = "No se pudo cargar el archivo."
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

    # --- Notas internas ---
    def construir_notas(filtro=""):
        lista_notas.controls.clear()
        archivos = listar_notas()
        filtro = (filtro or "").lower()
        encontrados = False

        if not archivos:
            lista_notas.controls.append(
                ft.Container(
                    content=ft.Text("No tienes notas.", size=16, color=ft.Colors.OUTLINE, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    height=120
                )
            )
        else:
            for archivo in sorted(archivos, key=lambda x: x.lower()):
                nombre_sin_ext = os.path.splitext(archivo)[0]
                if filtro in nombre_sin_ext.lower():
                    # usar mismo estilo que las perlas: tamaño, centrado y padding iguales
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
                            on_click=lambda e, a=archivo: ver_nota(a),
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=16),
                        elevation=2,
                    )
                    lista_notas.controls.append(card)
                    encontrados = True
            if not encontrados:
                lista_notas.controls.append(
                    ft.Container(
                        content=ft.Text("No se encontraron notas.", size=16, color=ft.Colors.OUTLINE, text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        height=120
                    )
                )

    def ver_nota(nombre_md):
        nonlocal mostrar_barra, current_view
        mostrar_barra = False
        current_view = "nota"
        ruta_md = os.path.join(RUTA_NOTAS, nombre_md)
        try:
            with open(ruta_md, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception:
            contenido = "No se pudo cargar la nota."
        lista_notas.controls.clear()
        lista_notas.controls.extend([
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

    # Buscador unificado (usado para Perlas y Notas según la pestaña)
    search_bar = ft.TextField(
        label="Buscar pearls...",
        on_change=lambda e: filter_current_value(e),
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.Colors.OUTLINE,
        bgcolor=ft.Colors.TRANSPARENT,
        filled=False,
        dense=True,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        width=400,
        expand=True,
    )

    # Barra fija superior (contiene solo el search bar de Perlas)
    barra_superior = ft.Container(
        content=ft.Row(
            controls=[search_bar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=10),
        alignment=ft.alignment.center,
    )

    # Áreas con scroll para cada pestaña
    area_perlas_scroll = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[lista_tarjetas],
            expand=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        ),
    )

    area_notas_scroll = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[lista_notas],
            expand=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        ),
    )

    # Pestañas internas: Perlas / Mis notas
    def on_tab_change(e):
        idx = e.control.selected_index
        if idx == 0:
            search_bar.label = "Buscar pearls..."
        else:
            search_bar.label = "Buscar notas..."
        # reaplicar el filtro actual (no limpiar el texto)
        filter_current_value()
        page.update()

    tabs = ft.Tabs(
        expand=True,
        on_change=on_tab_change,
        tabs=[
            ft.Tab(text="Perlas", content=ft.Column(controls=[area_perlas_scroll], expand=True)),
            ft.Tab(text="Mis notas", content=ft.Column(controls=[area_notas_scroll], expand=True)),
        ],
    )

    def actualizar_layout():
        layout_principal.controls.clear()
        if mostrar_barra and current_view == "tabs":
            # mostrar barra superior y las pestañas
            layout_principal.controls.extend([barra_superior, tabs])
        elif current_view == "perla":
            # mostrar solo la vista de perla (lista_tarjetas contiene el MD)
            layout_principal.controls.extend([area_perlas_scroll])
        elif current_view == "nota":
            # mostrar solo la vista de nota (lista_notas contiene el MD)
            layout_principal.controls.extend([area_notas_scroll])
        else:
            layout_principal.controls.extend([tabs])
        page.update()

    # Inicializar contenido
    construir_tarjetas()
    construir_notas()
    actualizar_layout()

    return layout_principal