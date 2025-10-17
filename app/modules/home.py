import os
import flet as ft
import re

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
    layout_principal = ft.Column(expand=True)

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
        filtro = (search_bar.value or "").strip()
        construir_tarjetas(filtro)

    def filtrar_notas(e):
        filtro = (search_bar.value or "").strip()
        construir_notas(filtro)

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
        construir_notas()
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

    def slugify(text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s]+", "_", text)
        return text or "nota"

    def open_note_editor(page: ft.Page, filename: str = None):
        is_new = filename is None
        title_val = ""
        content_val = ""
        if not is_new:
            ruta = os.path.join(RUTA_NOTAS, filename)
            try:
                title_val = os.path.splitext(filename)[0]
                with open(ruta, "r", encoding="utf-8") as f:
                    content_val = f.read()
            except Exception:
                title_val = os.path.splitext(filename)[0]
                content_val = ""

        tf_title = ft.TextField(label="Título", value=title_val, expand=True)
        tf_content = ft.TextField(label="Contenido (Markdown)", value=content_val, expand=True, multiline=True)

        templates = {
            "Seleccionar plantilla": "",
            "HC Medicina general": "## HISTORIA CLÍNICA - MEDICINA GENERAL\n\n### 1. Identificación\n- Nombre:\n- Edad:\n- Sexo:\n- Ocupación:\n- Estado civil:\n- Fecha de consulta:\n- Motivo de consulta:\n\n### 2. Historia de la enfermedad actual\n- Inicio:\n- Curso:\n- Síntomas principales:\n- Factores agravantes y atenuantes:\n- Tratamientos previos:\n\n### 3. Antecedentes personales\n- Patológicos:\n- Quirúrgicos:\n- Traumáticos:\n- Alérgicos:\n- Tóxicos:\n- Gineco-obstétricos (si aplica):\n\n### 4. Antecedentes familiares\n- Enfermedades hereditarias o familiares relevantes:\n\n### 5. Revisión por sistemas\n- Cabeza y cuello:\n- Respiratorio:\n- Cardiovascular:\n- Digestivo:\n- Genitourinario:\n- Músculo-esquelético:\n- Neurológico:\n\n### 6. Examen físico\n- Signos vitales:\n- General:\n- Cabeza y cuello:\n- Tórax:\n- Abdomen:\n- Extremidades:\n- Neurológico:\n\n### 7. Análisis / Impresión diagnóstica\n- Diagnóstico presuntivo:\n- Diagnóstico diferencial:\n\n### 8. Plan\n- Exámenes complementarios:\n- Tratamiento:\n- Educación al paciente:\n- Control y seguimiento:\n",
            "HC Pediatria": "## HISTORIA CLÍNICA - PEDIATRÍA\n\n### 1. Identificación\n- Nombre:\n- Edad:\n- Sexo:\n- Fecha de nacimiento:\n- Escolaridad:\n- Acompañante / cuidador:\n- Motivo de consulta:\n\n### 2. Antecedentes prenatales, natales y postnatales\n- Control prenatal:\n- Edad gestacional al nacer:\n- Tipo de parto:\n- Peso y talla al nacer:\n- Complicaciones perinatales:\n\n### 3. Antecedentes personales\n- Patológicos:\n- Quirúrgicos:\n- Alérgicos:\n- Alimentarios:\n- Vacunación:\n- Desarrollo psicomotor:\n\n### 4. Antecedentes familiares\n- Enfermedades hereditarias:\n- Antecedentes relevantes en padres o hermanos:\n\n### 5. Historia de la enfermedad actual (HEA)\n- Inicio y evolución:\n- Síntomas principales:\n- Factores asociados:\n- Tratamientos previos:\n\n### 6. Examen físico\n- Signos vitales:\n- Peso / talla / IMC / percentil:\n- Cabeza:\n- Tórax:\n- Abdomen:\n- Extremidades:\n- Neurológico:\n\n### 7. Análisis / Impresión diagnóstica\n- Diagnóstico presuntivo:\n- Diagnósticos diferenciales:\n\n### 8. Plan\n- Laboratorios y estudios:\n- Tratamiento farmacológico:\n- Recomendaciones nutricionales:\n- Seguimiento y controles:\n",
            "HC Ginecologia": "## HISTORIA CLÍNICA - GINECOLOGÍA\n\n### 1. Identificación\n- Nombre:\n- Edad:\n- Estado civil:\n- Ocupación:\n- Fecha de consulta:\n- Motivo de consulta:\n\n### 2. Antecedentes gineco-obstétricos\n- Menarquia:\n- Ciclo menstrual:\n- FUR (Fecha de última regla):\n- FUP (Fecha de última citología / papanicolau):\n- Gestaciones:\n- Partos:\n- Abortos:\n- Métodos anticonceptivos:\n- Vida sexual activa (VSA):\n\n### 3. Antecedentes personales y familiares\n- Patológicos:\n- Quirúrgicos:\n- Alérgicos:\n- Familiares:\n\n### 4. Historia de la enfermedad actual\n- Inicio y evolución:\n- Síntomas principales (flujo, dolor, sangrado, etc.):\n- Factores asociados:\n- Tratamientos previos:\n\n### 5. Examen físico\n- Signos vitales:\n- Mamas:\n- Abdomen:\n- Examen pélvico:\n- Especuloscopia:\n- Tacto bimanual:\n\n### 6. Análisis / Impresión diagnóstica\n- Diagnóstico presuntivo:\n- Diagnóstico diferencial:\n\n### 7. Plan\n- Estudios de laboratorio o imagen:\n- Tratamiento médico / quirúrgico:\n- Consejería y educación sexual:\n- Seguimiento:\n",
        }


        template_dropdown = ft.Dropdown(
            label="Plantilla",
            options=[ft.dropdown.Option(k) for k in templates.keys()],
            value="Seleccionar plantilla",
            width=True,
            expand=True,
        )

        def on_template_change(e):
            sel = (e.control.value or "")
            tpl_text = templates.get(sel, "")
            if not tpl_text:
                return
            if not (tf_content.value or "").strip():
                tf_content.value = tpl_text
            else:
                tf_content.value = (tf_content.value or "") + "\n\n" + tpl_text
            page.update()

        template_dropdown.on_change = on_template_change

        error_text = ft.Text("", size=12, color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)

        content_list = ft.ListView(
            expand=True,
            padding=ft.padding.all(8),
            spacing=8,
            controls=[
                ft.Container(content=error_text, alignment=ft.alignment.center, height=28),
                template_dropdown,
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
                    content=ft.Text("No tienes notas.", size=16, color=ft.Colors.OUTLINE, text_align=ft.TextAlign.CENTER),
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
            controls=[search_bar],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=40, vertical=10),
        alignment=ft.alignment.center,
    )

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

    def on_tab_change(e):
        idx = e.control.selected_index
        if idx == 0:
            search_bar.label = "Buscar pearls..."
            try:
                row = barra_superior.content
                if btn_new_nota in row.controls:
                    row.controls.remove(btn_new_nota)
            except Exception:
                pass
        else:
            search_bar.label = "Buscar notas..."
            try:
                row = barra_superior.content
                if btn_new_nota not in row.controls:
                    row.controls.append(btn_new_nota)
            except Exception:
                pass
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
            layout_principal.controls.extend([barra_superior, tabs])
        elif current_view == "perla":
            layout_principal.controls.extend([area_perlas_scroll])
        elif current_view == "nota":
            layout_principal.controls.extend([area_notas_scroll])
        else:
            layout_principal.controls.extend([tabs])
        page.update()

    construir_tarjetas()
    construir_notas()
    actualizar_layout()

    return layout_principal