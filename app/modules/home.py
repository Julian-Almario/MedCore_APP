import os
import flet as ft
import re

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

    # Search bar unificado (debe definirse antes de las funciones que lo usan)
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
    # helper: slugify para nombres de archivo seguros
    def slugify(text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s]+", "_", text)
        return text or "nota"

    # ---- Editor de notas (crear / editar) ----
    def open_note_editor(page: ft.Page, filename: str = None):
        # filename: nombre del archivo con extensión o None para nueva nota
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

        # Plantillas predeterminadas para el contenido
        templates = {
            "Seleccionar plantilla": "",

            "HC Medicina general": "## HISTORIA CLÍNICA - MEDICINA GENERAL\n\n### 1. Identificación\n- Nombre:\n- Edad:\n- Sexo:\n- Ocupación:\n- Estado civil:\n- Fecha de consulta:\n- Motivo de consulta:\n\n### 2. Historia de la enfermedad actual (HEA)\n- Inicio:\n- Curso:\n- Síntomas principales:\n- Factores agravantes y atenuantes:\n- Tratamientos previos:\n\n### 3. Antecedentes personales\n- Patológicos:\n- Quirúrgicos:\n- Traumáticos:\n- Alérgicos:\n- Tóxicos:\n- Gineco-obstétricos (si aplica):\n\n### 4. Antecedentes familiares\n- Enfermedades hereditarias o familiares relevantes:\n\n### 5. Revisión por sistemas\n- Cabeza y cuello:\n- Respiratorio:\n- Cardiovascular:\n- Digestivo:\n- Genitourinario:\n- Músculo-esquelético:\n- Neurológico:\n\n### 6. Examen físico\n- Signos vitales:\n- General:\n- Cabeza y cuello:\n- Tórax:\n- Abdomen:\n- Extremidades:\n- Neurológico:\n\n### 7. Análisis / Impresión diagnóstica\n- Diagnóstico presuntivo:\n- Diagnóstico diferencial:\n\n### 8. Plan\n- Exámenes complementarios:\n- Tratamiento:\n- Educación al paciente:\n- Control y seguimiento:\n",

            "HC Pediatria": "## HISTORIA CLÍNICA - PEDIATRÍA\n\n### 1. Identificación\n- Nombre:\n- Edad:\n- Sexo:\n- Fecha de nacimiento:\n- Escolaridad:\n- Acompañante / cuidador:\n- Motivo de consulta:\n\n### 2. Antecedentes prenatales, natales y postnatales\n- Control prenatal:\n- Edad gestacional al nacer:\n- Tipo de parto:\n- Peso y talla al nacer:\n- Complicaciones perinatales:\n\n### 3. Antecedentes personales\n- Patológicos:\n- Quirúrgicos:\n- Alérgicos:\n- Alimentarios:\n- Vacunación:\n- Desarrollo psicomotor:\n\n### 4. Antecedentes familiares\n- Enfermedades hereditarias:\n- Antecedentes relevantes en padres o hermanos:\n\n### 5. Historia de la enfermedad actual (HEA)\n- Inicio y evolución:\n- Síntomas principales:\n- Factores asociados:\n- Tratamientos previos:\n\n### 6. Examen físico\n- Signos vitales:\n- Peso / talla / IMC / percentil:\n- Cabeza:\n- Tórax:\n- Abdomen:\n- Extremidades:\n- Neurológico:\n\n### 7. Análisis / Impresión diagnóstica\n- Diagnóstico presuntivo:\n- Diagnósticos diferenciales:\n\n### 8. Plan\n- Laboratorios y estudios:\n- Tratamiento farmacológico:\n- Recomendaciones nutricionales:\n- Seguimiento y controles:\n",

            "HC Ginecologia": "## HISTORIA CLÍNICA - GINECOLOGÍA\n\n### 1. Identificación\n- Nombre:\n- Edad:\n- Estado civil:\n- Ocupación:\n- Fecha de consulta:\n- Motivo de consulta:\n\n### 2. Antecedentes gineco-obstétricos\n- Menarquia:\n- Ciclo menstrual:\n- FUR (Fecha de última regla):\n- FUP (Fecha de última citología / papanicolau):\n- Gestaciones:\n- Partos:\n- Abortos:\n- Métodos anticonceptivos:\n- Vida sexual activa (VSA):\n\n### 3. Antecedentes personales y familiares\n- Patológicos:\n- Quirúrgicos:\n- Alérgicos:\n- Familiares:\n\n### 4. Historia de la enfermedad actual\n- Inicio y evolución:\n- Síntomas principales (flujo, dolor, sangrado, etc.):\n- Factores asociados:\n- Tratamientos previos:\n\n### 5. Examen físico\n- Signos vitales:\n- Mamas:\n- Abdomen:\n- Examen pélvico:\n- Especuloscopia:\n- Tacto bimanual:\n\n### 6. Análisis / Impresión diagnóstica\n- Diagnóstico presuntivo:\n- Diagnóstico diferencial:\n\n### 7. Plan\n- Estudios de laboratorio o imagen:\n- Tratamiento médico / quirúrgico:\n- Consejería y educación sexual:\n- Seguimiento:\n",
        }



        # Dropdown de plantillas
        template_dropdown = ft.Dropdown(
            label="Plantilla",
            options=[ft.dropdown.Option(k) for k in templates.keys()],
            value="Seleccionar plantilla",
            width=True,
            expand=True,
        )

        def on_template_change(e):
            sel = (e.control.value or "")
            # si hay contenido existente y se está editando, preguntar si sobrescribir?
            # comportamiento: si tf_content está vacío o viene de la plantilla, reemplaza; si tiene texto no vacío concatena
            tpl_text = templates.get(sel, "")
            if not tpl_text:
                return
            # si el contenido actual es vacío o igual a la plantilla previa, reemplazar; en otro caso preguntar por concatenar
            if not (tf_content.value or "").strip():
                tf_content.value = tpl_text
            else:
                # concatenar la plantilla al contenido existente para no perder texto
                tf_content.value = (tf_content.value or "") + "\n\n" + tpl_text
            page.update()

        template_dropdown.on_change = on_template_change

        # Scroll interno para evitar recortes
        content_list = ft.ListView(
            expand=True,
            padding=ft.padding.all(8),
            spacing=8,
            controls=[template_dropdown, tf_title, tf_content],
        )

        def guardar(e):
            titulo = (tf_title.value or "").strip()
            if not titulo:
                dlg_err = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("El título es obligatorio."),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_err))],
                    modal=True,
                )
                page.open(dlg_err)
                return

            base_name = slugify(titulo)
            destino = base_name + ".md"
            # si es nueva nota y ya existe, añadir sufijo incremental
            if is_new:
                i = 1
                while os.path.exists(os.path.join(RUTA_NOTAS, destino)):
                    destino = f"{base_name}_{i}.md"
                    i += 1
            else:
                # si renombró el título, actualizar nombre; evitar sobrescribir otra nota
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
                # si se renombró (editar con cambio de nombre), remover el antiguo
                if not is_new and filename and destino != filename:
                    try:
                        os.remove(os.path.join(RUTA_NOTAS, filename))
                    except Exception:
                        pass
                page.close(dlg)
                construir_notas()
                mostrar_lista()
            except Exception as ex:
                dlg_err = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("No se pudo guardar la nota."),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_err))],
                    modal=True,
                )
                page.open(dlg_err)

        dlg = ft.AlertDialog(
            title=ft.Text("Nueva nota" if is_new else f"Editar nota: {os.path.splitext(filename)[0]}"),
            content=ft.Container(content=content_list, width=700, height=480),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)), ft.ElevatedButton("Guardar", on_click=guardar)],
            modal=True,
        )
        page.open(dlg)

    # ---- Confirmar y eliminar nota ----
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
                # botones editar / eliminar en la cabecera de la nota
                ft.Container( expand=True ),
                ft.IconButton( ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, a=nombre_md: open_note_editor(page, filename=a) ),
                ft.IconButton( ft.Icons.DELETE, tooltip="Eliminar", on_click=lambda e, a=nombre_md: confirm_delete_note(page, filename=a), icon_color=ft.Colors.RED_700),
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

    # añadir botón rápido para nueva nota en la cabecera (junto al search_bar)
    btn_new_nota = ft.IconButton(
        icon=ft.Icons.ADD,
        tooltip="Nueva nota",
        on_click=lambda e: open_note_editor(page, filename=None),
    )

    # Barra superior inicial solo con el search_bar.
    # El botón de nueva nota se añadirá/quitará según la pestaña activa en on_tab_change.
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
            # quitar el botón de nueva nota si está presente
            try:
                row = barra_superior.content
                if btn_new_nota in row.controls:
                    row.controls.remove(btn_new_nota)
            except Exception:
                pass
        else:
            search_bar.label = "Buscar notas..."
            # añadir el botón de nueva nota si no está ya
            try:
                row = barra_superior.content
                if btn_new_nota not in row.controls:
                    row.controls.append(btn_new_nota)
            except Exception:
                pass
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