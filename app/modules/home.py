import os
import flet as ft
import re

RUTA_NOTAS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "notas"))
os.makedirs(RUTA_NOTAS, exist_ok=True)

def listar_notas():
    return [f for f in os.listdir(RUTA_NOTAS) if f.lower().endswith(".md")]

def pantalla_home(page: ft.Page):
    lista_notas = ft.Column(spacing=10, expand=True)
    mostrar_barra = True
    current_view = "notas"
    layout_principal = ft.Column(expand=True)

    search_bar = ft.TextField(
        label="Buscar notas...",
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

    def filter_current_value(_e=None):
        valor = (search_bar.value or "").strip()
        construir_notas(valor)
        page.update()

    def mostrar_lista():
        nonlocal mostrar_barra, current_view
        mostrar_barra = True
        current_view = "notas"
        construir_notas()
        actualizar_layout()

    def slugify(text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s]+", "_", text)
        return text or "nota"

    def pretty_title(filename: str) -> str:
        root = os.path.splitext(filename)[0]
        return re.sub(r'[_]+', ' ', root).strip()

    def open_note_editor(page: ft.Page, filename: str = None):
        is_new = filename is None
        title_val = ""
        content_val = ""
        if not is_new:
            ruta = os.path.join(RUTA_NOTAS, filename)
            try:
                title_val = pretty_title(filename)
                with open(ruta, "r", encoding="utf-8") as f:
                    content_val = f.read()
            except Exception:
                title_val = pretty_title(filename)
                content_val = ""

        tf_title = ft.TextField(label="Título", value=title_val, expand=True)
        tf_content = ft.TextField(label="Contenido (Markdown)", value=content_val, expand=True, multiline=True)

        error_text = ft.Text("", size=12, color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)

        content_list = ft.ListView(
            expand=True,
            padding=ft.padding.all(8),
            spacing=8,
            controls=[
                ft.Container(content=error_text, alignment=ft.alignment.center, height=28),
                tf_title,
                tf_content
            ],
        )

        closed_properly = [False]

        def guardar(e):
            titulo = (tf_title.value or "").strip()
            if not titulo:
                error_text.value = "Introduce un título antes de guardar."
                page.update()
                return
            error_text.value = ""
            base_name = slugify(titulo)
            destino = base_name + ".md"
            if is_new:
                i = 1
                while os.path.exists(os.path.join(RUTA_NOTAS, destino)):
                    destino = f"{base_name}_{i}.md"
                    i += 1
            else:
                if destino != filename:
                    if os.path.exists(os.path.join(RUTA_NOTAS, destino)):
                        i = 1
                        new_dest = f"{base_name}_{i}.md"
                        while os.path.exists(os.path.join(RUTA_NOTAS, new_dest)):
                            i += 1
                            new_dest = f"{base_name}_{i}.md"
                        destino = new_dest
            try:
                os.makedirs(RUTA_NOTAS, exist_ok=True)
                with open(os.path.join(RUTA_NOTAS, destino), "w", encoding="utf-8") as f:
                    f.write(tf_content.value or "")
                if not is_new and filename and destino != filename:
                    try:
                        os.remove(os.path.join(RUTA_NOTAS, filename))
                    except Exception:
                        pass
                closed_properly[0] = True
                page.close(dlg)
                construir_notas()
                mostrar_lista()
            except Exception:
                dlg_err = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("No se pudo guardar la nota."),
                    actions=[ft.TextButton("Cerrar", on_click=lambda ev: page.close(dlg_err))],
                    modal=True,
                )
                page.open(dlg_err)

        def cancelar(e):
            closed_properly[0] = True
            page.close(dlg)

        def on_dismiss_handler(e):
            if not closed_properly[0]:
                try:
                    page.open(dlg)
                except Exception:
                    pass

        dlg = ft.AlertDialog(
            title=ft.Text("Nueva nota" if is_new else f"Editar nota: {os.path.splitext(filename)[0]}"),
            content=ft.Container(content=content_list, width=700, height=480),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar", on_click=guardar)
            ],
            modal=True,
            on_dismiss=on_dismiss_handler,
        )
        page.open(dlg)

    def confirm_delete_note(page: ft.Page, filename: str):
        def eliminar(e):
            try:
                os.remove(os.path.join(RUTA_NOTAS, filename))
            except Exception:
                pass
            page.close(dlg)
            construir_notas()
            mostrar_lista()

        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Eliminar la nota '{os.path.splitext(filename)[0]}'?"),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)), ft.TextButton("Eliminar", on_click=eliminar)],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
        )
        page.open(dlg)

    def construir_notas(filtro=""):
        lista_notas.controls.clear()
        archivos = listar_notas()
        filtro = (filtro or "").lower()
        encontrados = False

        if not archivos:
            lista_notas.controls.append(
                ft.Container(
                    content=ft.Text("No tienes notas. Crea una nueva nota con el botón '+'", size=16, color=ft.Colors.OUTLINE, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    height=120
                )
            )
            return

        for archivo in sorted(archivos, key=lambda x: x.lower()):
            nombre_sin_ext = os.path.splitext(archivo)[0]
            nombre_busqueda = re.sub(r'[_]+', ' ', nombre_sin_ext).lower()
            if filtro and filtro not in nombre_busqueda:
                continue

            card = ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(pretty_title(archivo), size=18, text_align=ft.TextAlign.CENTER),
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
                    content=ft.Text("No hay notas que coincidan con la búsqueda.", size=16, color=ft.Colors.OUTLINE, text_align=ft.TextAlign.CENTER),
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
                ft.Text(pretty_title(nombre_md), size=22),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, a=nombre_md: open_note_editor(page, filename=a)),
                ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", on_click=lambda e, a=nombre_md: confirm_delete_note(page, filename=a), icon_color=ft.Colors.RED_700),
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

    btn_new_nota = ft.IconButton(
        icon=ft.Icons.ADD,
        tooltip="Nueva nota",
        on_click=lambda e: open_note_editor(page, filename=None),
    )

    barra_superior = ft.Container(
        content=ft.Row(
            controls=[search_bar, btn_new_nota],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=10),
        alignment=ft.alignment.center,
    )

    area_notas_scroll = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[lista_notas],
            expand=True,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        ),
    )

    def actualizar_layout():
        layout_principal.controls.clear()
        if mostrar_barra and current_view == "notas":
            layout_principal.controls.extend([barra_superior, area_notas_scroll])
        elif current_view == "nota":
            layout_principal.controls.extend([area_notas_scroll])
        page.update()

    construir_notas()
    actualizar_layout()

    return layout_principal