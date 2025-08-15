import os
import json
import flet as ft
from datetime import date

# Ruta de almacenamiento
RUTA_HISTORIAS = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "storage", "data", "historias")
)
os.makedirs(RUTA_HISTORIAS, exist_ok=True)
ARCHIVO_HISTORIAS = os.path.join(RUTA_HISTORIAS, "historias.json")

# Crear archivo vacío si no existe
if not os.path.exists(ARCHIVO_HISTORIAS):
    with open(ARCHIVO_HISTORIAS, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

def cargar_historias():
    try:
        with open(ARCHIVO_HISTORIAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_todas_las_historias(historias):
    with open(ARCHIVO_HISTORIAS, "w", encoding="utf-8") as f:
        json.dump(historias, f, ensure_ascii=False, indent=4)

def guardar_historia_en_json(historia: dict):
    historias = cargar_historias()
    historias.append(historia)
    guardar_todas_las_historias(historias)

def _panel_de_historia(hist: dict, index: int, refrescar_lista, page) -> ft.ExpansionPanel:
    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        if panel:
            panel.bgcolor = "#2E2E2E" if panel.expanded else "#1E1E1E"
            panel.update()

    # Acción borrar
    def borrar_historia_click(e):
        historias = cargar_historias()
        del historias[index]
        guardar_todas_las_historias(historias)
        refrescar_lista()
        page.snack_bar = ft.SnackBar(ft.Text("Historia eliminada"), open=True)
        page.update()

    # Acción editar
    def editar_historia_click(e):
        mostrar_formulario_historia(page, refrescar_lista, historia_existente=hist, index=index)

    contenido_panel = [
        ft.Text(f"Fecha: {hist.get('fecha', 'N/A')}"),
        ft.Text(f"Motivo de consulta: {hist.get('motivo', '')}"),
        ft.Text(f"Resumen: {hist.get('resumen', '')}"),
        ft.Row([
            ft.ElevatedButton("✏️ Editar", on_click=editar_historia_click),
            ft.ElevatedButton("🗑️ Borrar", on_click=borrar_historia_click, bgcolor="red", color="white")
        ])
    ]

    extra = hist.get("extra", {})
    if extra:
        contenido_panel.insert(-1, ft.Text("Campos adicionales:", weight=ft.FontWeight.BOLD))
        for clave, valor in extra.items():
            contenido_panel.insert(-1, ft.Text(f"{clave}: {valor}"))

    return ft.ExpansionPanel(
        ref=panel_ref,
        header=ft.ListTile(
            title=ft.Text(hist.get("nombre", "Sin nombre")),
            subtitle=ft.Text(f"{hist.get('formato', 'N/A')} · {hist.get('identificacion', '')}"),
        ),
        content=ft.Container(content=ft.Column(controls=contenido_panel), padding=15),
        bgcolor="#1E1E1E",
        expanded=False,
    )

def mostrar_formulario_historia(page, refrescar_lista, historia_existente=None, index=None):
    historia_existente = historia_existente or {}

    formato_dropdown = ft.Dropdown(
        label="Formato de historia clínica",
        options=[
            ft.dropdown.Option("Medicina General"),
            ft.dropdown.Option("Pediatría"),
            ft.dropdown.Option("Ginecología"),
        ],
        width=300,
        value=historia_existente.get("formato")
    )

    nombre_input = ft.TextField(label="Nombre del paciente", width=300, value=historia_existente.get("nombre", ""))
    id_input = ft.TextField(label="Identificación", width=200, value=historia_existente.get("identificacion", ""))
    motivo_input = ft.TextField(label="Motivo de consulta", multiline=True, width=400, value=historia_existente.get("motivo", ""))
    resumen_input = ft.TextField(label="Resumen", multiline=True, width=400, value=historia_existente.get("resumen", ""))

    campos_extra = ft.Column()
    extra_data = historia_existente.get("extra", {})

    def actualizar_campos_extra(ev):
        # Guardar valores actuales antes de regenerar
        valores_actuales = {}
        for campo in campos_extra.controls:
            if isinstance(campo, ft.TextField):
                valores_actuales[campo.label] = campo.value or ""

        campos_extra.controls.clear()

        def valor_guardado(clave):
            return valores_actuales.get(clave, extra_data.get(clave, ""))

        if formato_dropdown.value == "Ginecología":
            campos_extra.controls.extend([
                ft.TextField(label="Gestas", width=150, value=valor_guardado("Gestas")),
                ft.TextField(label="Partos", width=150, value=valor_guardado("Partos")),
                ft.TextField(label="Abortos", width=150, value=valor_guardado("Abortos")),
                ft.TextField(label="Cesáreas", width=150, value=valor_guardado("Cesáreas")),
                ft.TextField(label="FUM (Fecha Última Menstruación)", width=200, value=valor_guardado("FUM (Fecha Última Menstruación)")),
            ])
        elif formato_dropdown.value == "Pediatría":
            campos_extra.controls.extend([
                ft.TextField(label="Edad gestacional al nacer", width=200, value=valor_guardado("Edad gestacional al nacer")),
                ft.TextField(label="Peso al nacer", width=150, value=valor_guardado("Peso al nacer")),
                ft.TextField(label="Talla al nacer", width=150, value=valor_guardado("Talla al nacer")),
                ft.TextField(label="APGAR 1 min", width=150, value=valor_guardado("APGAR 1 min")),
                ft.TextField(label="APGAR 5 min", width=150, value=valor_guardado("APGAR 5 min")),
            ])
        elif formato_dropdown.value == "Medicina General":
            campos_extra.controls.extend([
                ft.TextField(label="Antecedentes personales", multiline=True, width=400, value=valor_guardado("Antecedentes personales")),
                ft.TextField(label="Antecedentes familiares", multiline=True, width=400, value=valor_guardado("Antecedentes familiares")),
            ])
        elif formato_dropdown.value == "Otro":
            campos_extra.controls.append(
                ft.TextField(label="Observaciones especiales", multiline=True, width=400, value=valor_guardado("Observaciones especiales"))
            )

        # Solo actualizamos si el control ya está en pantalla
        if campos_extra.page is not None:
            campos_extra.update()


    formato_dropdown.on_change = actualizar_campos_extra
    if historia_existente:
        actualizar_campos_extra(None)

    def guardar_click(ev):
        historia = {
            "formato": formato_dropdown.value or "Medicina General",
            "nombre": (nombre_input.value or "").strip(),
            "identificacion": (id_input.value or "").strip(),
            "motivo": (motivo_input.value or "").strip(),
            "resumen": (resumen_input.value or "").strip(),
            "fecha": str(date.today()),
            "extra": {}
        }

        for campo in campos_extra.controls:
            if isinstance(campo, ft.TextField):
                historia["extra"][campo.label] = (campo.value or "").strip()

        historias = cargar_historias()
        if index is not None:
            historias[index] = historia
        else:
            historias.append(historia)
        guardar_todas_las_historias(historias)

        refrescar_lista()
        page.close(dialogo)
        page.snack_bar = ft.SnackBar(ft.Text("Historia guardada correctamente"), open=True)
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Historia Clínica" if historia_existente else "Nueva Historia Clínica"),
        content=ft.Column(
            controls=[
                formato_dropdown,
                nombre_input,
                id_input,
                motivo_input,
                resumen_input,
                campos_extra,
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda ev: page.close(dialogo)),
            ft.TextButton("Guardar", on_click=guardar_click),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    page.dialog = dialogo
    page.open(dialogo)

def pantalla_historia_clinica(page: ft.Page):
    lista_panels = ft.ExpansionPanelList(expand_icon_color=ft.Colors.WHITE, elevation=8)

    def refrescar_lista():
        lista_panels.controls.clear()
        for idx, hist in enumerate(cargar_historias()):
            lista_panels.controls.append(_panel_de_historia(hist, idx, refrescar_lista, page))
        try:
            lista_panels.update()
        except AssertionError:
            pass

    refrescar_lista()

    encabezado = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(height=50),
                ft.Container(
                    content=ft.Text(
                        "Mi archivo clínico",
                        size=25,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        expand=True
                    ),
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ADD,
                        icon_color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE,
                        on_click=lambda e: mostrar_formulario_historia(page, refrescar_lista),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=100),
                            padding=10
                        ),
                        tooltip="Crear nueva historia",
                    ),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(16),
        margin=ft.margin.only(top=10, bottom=20),
        alignment=ft.alignment.center
    )

    return ft.Column(
        expand=True,
        controls=[
            encabezado,
            ft.Container(
                expand=True,
                content=ft.ListView(
                    expand=True,
                    controls=[lista_panels],
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                ),
            ),
        ],
    )
