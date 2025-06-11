import flet as ft
from modules.colors import *

def presion_arterial_media():
    sistolica_field = ft.TextField(
        label="Presión Sistólica (mmHg)",
        hint_text="Ej: 120",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    diastolica_field = ft.TextField(
        label="Presión Diastólica (mmHg)",
        hint_text="Ej: 80",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    resultado_texto = ft.Text(
        "PAM: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    formula_text = ft.Text(
        "Fórmula usada: PAM = (2 x PAD + PAS) / 3",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_pam(e):
        try:
            pas = float(sistolica_field.value)
            pad = float(diastolica_field.value)

            pam = (2 * pad + pas) / 3
            resultado_texto.value = f"PAM: {pam:.2f} mmHg"
            formula_text.value = f"Fórmula usada: PAM = (2 x {pad} + {pas}) / 3 = {pam:.2f}"

        except ValueError:
            resultado_texto.value = "PAM: Valor inválido"
            formula_text.value = "Fórmula usada: PAM = (2 x PAD + PAS) / 3"

        resultado_texto.update()
        formula_text.update()

    sistolica_field.on_change = calcular_pam
    diastolica_field.on_change = calcular_pam

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            sistolica_field.value = ""
            diastolica_field.value = ""
            resultado_texto.value = "PAM: -"
            formula_text.value = "Fórmula usada: PAM = (2 x PAD + PAS) / 3"
            sistolica_field.update()
            diastolica_field.update()
            resultado_texto.update()
            formula_text.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Presión Arterial Media (PAM)", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Column(
                                controls=[
                                    sistolica_field,
                                    diastolica_field,
                                ],
                                spacing=8,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row([formula_text], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([resultado_texto], alignment=ft.MainAxisAlignment.CENTER)
                        ],
                        spacing=15,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(10)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

def criterios_wells_tvp():
    criterios = [
        ("Cáncer activo (tratamiento en curso o en los últimos 6 meses)", 1),
        ("Parálisis, paresia o inmovilización de extremidad inferior", 1),
        ("Reposo en cama > 3 días o cirugía reciente en extremidad inferior", 1),
        ("Dolor localizado a lo largo del trayecto venoso profundo", 1),
        ("Edema distal unilateral de toda la pierna", 1),
        ("Edema de pantorrilla > 3 cm comparado con la pierna contralateral", 1),
        ("Piel caliente en extremidad afectada", 1),
        ("Venas colaterales superficiales no varicosas", 1),
        ("Diagnóstico alternativo tan probable o más probable que TVP", -2),
    ]

    checkboxes = []

    resultado_texto = ft.Text(
        "Puntaje Wells: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    riesgo_texto = ft.Text(
        "",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_wells(e=None):
        puntaje = sum(valor for cb, valor in checkboxes if cb.value)
        resultado_texto.value = f"Puntaje Wells: {puntaje}"

        if puntaje >= 3:
            riesgo = "Alto riesgo de TVP"
            riesgo_texto.color = "red"
        elif 1 <= puntaje < 3:
            riesgo = "Riesgo moderado de TVP"
            riesgo_texto.color = "orange"
        else:
            riesgo = "Bajo riesgo de TVP"
            riesgo_texto.color = "green"

        riesgo_texto.value = riesgo
        resultado_texto.update()
        riesgo_texto.update()


    def construir_tabla(criterios, checkboxes):
        filas = []
        for texto, valor in criterios:
            chk = ft.Checkbox(value=False, on_change=calcular_wells)
            checkboxes.append((chk, valor))
            fila = ft.Row(
                controls=[
                    ft.Container(ft.Text(texto, color=TEXT_COLOR), expand=True),
                    ft.Container(ft.Text(f"{valor:+}", color=TEXT_COLOR), width=30, alignment=ft.alignment.center_right),
                    ft.Container(chk, alignment=ft.alignment.center_right)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            filas.append(fila)
        return filas

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            for cb, _ in checkboxes:
                cb.value = False
                cb.update()
            resultado_texto.value = "Puntaje Wells: -"
            riesgo_texto.value = ""
            resultado_texto.update()
            riesgo_texto.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Criterios de Wells para TVP", color=TEXT_COLOR),
                    subtitle=ft.Text("Probabilidad de paciente con TVP", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            *construir_tabla(criterios, checkboxes),
                            ft.Divider(),
                            resultado_texto,
                            riesgo_texto
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=45),
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ]
    )


def criterios_wells_tep():
    criterios = [
        ("Signos clínicos de TVP (dolor, edema, etc.)", 3),
        ("Diagnóstico alternativo menos probable que embolia pulmonar", 3),
        ("Frecuencia cardíaca > 100 lpm", 1.5),
        ("Inmovilización o cirugía en las últimas 4 semanas", 1.5),
        ("Antecedente previo de TVP o EP", 1.5),
        ("Hemoptisis", 1),
        ("Cáncer activo (tratamiento en curso o en los últimos 6 meses)", 1),
    ]

    checkboxes = []

    resultado_texto = ft.Text(
        "Puntaje Wells EP: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    riesgo_texto = ft.Text(
        "",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_wells_ep(e=None):
        puntaje = sum(valor for cb, valor in checkboxes if cb.value)
        resultado_texto.value = f"Puntaje Wells EP: {puntaje:.1f}"

        if puntaje > 6:
            riesgo = "Alto riesgo de embolia pulmonar"
            riesgo_texto.color = "red"
        elif 2 <= puntaje <= 6:
            riesgo = "Riesgo intermedio de embolia pulmonar"
            riesgo_texto.color = "orange"
        else:
            riesgo = "Bajo riesgo de embolia pulmonar"
            riesgo_texto.color = "green"

        riesgo_texto.value = riesgo
        resultado_texto.update()
        riesgo_texto.update()


    def construir_tabla(criterios, checkboxes):
        filas = []
        for texto, valor in criterios:
            chk = ft.Checkbox(value=False, on_change=calcular_wells_ep)
            checkboxes.append((chk, valor))
            fila = ft.Row(
                controls=[
                    ft.Container(ft.Text(texto, color=TEXT_COLOR), expand=True),
                    ft.Container(ft.Text(f"{valor:+.1f}", color=TEXT_COLOR), width=30, alignment=ft.alignment.center_right),
                    ft.Container(chk, alignment=ft.alignment.center_right)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            filas.append(fila)
        return filas

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            for cb, _ in checkboxes:
                cb.value = False
                cb.update()
            resultado_texto.value = "Puntaje Wells EP: -"
            riesgo_texto.value = ""
            resultado_texto.update()
            riesgo_texto.update()

    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Criterios de Wells para Embolia Pulmonar", color=TEXT_COLOR),
                    subtitle=ft.Text("Probabilidad de paciente con TEP", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            *construir_tabla(criterios, checkboxes),
                            ft.Divider(),
                            resultado_texto,
                            riesgo_texto
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=45),
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ]
    )
