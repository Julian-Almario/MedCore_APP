import flet as ft
from modules.colors import *

def tfg_schwartz():
    altura_field = ft.TextField(
        label="Altura (cm)",
        hint_text="Ej: 60",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    creatinina_field = ft.TextField(
        label="Creatinina sérica (mg/dL)",
        hint_text="Ej: 0.8",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    k_selector = ft.Dropdown(
        label="Tipo de paciente",
        options=[
            ft.dropdown.Option("Término k = 0.33"),
            ft.dropdown.Option("Prematuro k = 0.45")
        ],
        value="Término k = 0.33",
        width=250
    )

    resultado_texto = ft.Text(
        "TFGe: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    formula_text = ft.Text(
        "Fórmula usada: TFGe = (k x Altura) / Creatinina",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_tfge(e):
        try:
            altura = float(altura_field.value)
            creatinina = float(creatinina_field.value)
            k = 0.33 if k_selector.value == "Término k = 0.33" else 0.45

            if creatinina == 0:
                raise ZeroDivisionError

            tfge = (k * altura) / creatinina
            resultado_texto.value = f"TFGe: {tfge:.2f} mL/min/1.73m²"
            formula_text.value = f"Fórmula usada: TFGe = ({k} × {altura}) / {creatinina} = {tfge:.2f}"
        except (ValueError, ZeroDivisionError):
            resultado_texto.value = "TFGe: Valor inválido"
            formula_text.value = "Fórmula usada: TFGe = k × Altura / Creatinina"

        resultado_texto.update()
        formula_text.update()

    altura_field.on_change = calcular_tfge
    creatinina_field.on_change = calcular_tfge
    k_selector.on_change = calcular_tfge

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            altura_field.value = ""
            creatinina_field.value = ""
            k_selector.value = "Término k = 0.33"
            resultado_texto.value = "TFGe: -"
            formula_text.value = "Fórmula usada: TFGe = (k x Altura) / Creatinina"
            altura_field.update()
            creatinina_field.update()
            k_selector.update()
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
                    title=ft.Text("TFG Ecuación de Schwartz 2009", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([formula_text], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column(
                                controls=[
                                    altura_field,
                                    creatinina_field,
                                    k_selector,
                                ],
                                spacing=8,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
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

def ckd_epi_2021():
    sexo = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")],
        width=200
    )

    edad = ft.TextField(label="Edad (años)", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    creatinina = ft.TextField(label="Creatinina (mg/dL)", keyboard_type=ft.KeyboardType.NUMBER, width=200)

    resultado_ckd = ft.Text("eGFR (CKD-EPI 2021): -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_ckd = ft.Text("Clasificación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_ckd(e):
        try:
            age = float(edad.value.replace(',', '.'))
            cr = float(creatinina.value.replace(',', '.'))
            sex = sexo.value

            if sex == "Femenino":
                k = 0.7
                alpha = -0.241
                mult = 1.012
            else:
                k = 0.9
                alpha = -0.302
                mult = 1.0

            egfr = 142 * min(cr / k, 1)**alpha * max(cr / k, 1)**-1.200 * 0.9938**age * mult
            egfr = round(egfr, 1)

            resultado_ckd.value = f"eGFR (CKD-EPI 2021): {egfr} mL/min/1.73m²"

            if egfr >= 90:
                categoria = "G1: Función normal"
            elif egfr >= 60:
                categoria = "G2: Leve disminución"
            elif egfr >= 45:
                categoria = "G3a: Disminución leve-moderada"
            elif egfr >= 30:
                categoria = "G3b: Disminución moderada-severa"
            elif egfr >= 15:
                categoria = "G4: Disminución severa"
            else:
                categoria = "G5: Falla renal"

            interpretacion_ckd.value = f"Clasificación: {categoria}"

        except Exception:
            resultado_ckd.value = "eGFR (CKD-EPI 2021): -"
            interpretacion_ckd.value = "Clasificación: Datos inválidos"

        resultado_ckd.update()
        interpretacion_ckd.update()

    for field in [sexo, edad, creatinina]:
        field.on_change = calcular_ckd

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            sexo.value = None
            edad.value = ""
            creatinina.value = ""
            for field in [sexo, edad, creatinina]:
                field.update()
            resultado_ckd.value = "eGFR (CKD-EPI 2021): -"
            interpretacion_ckd.value = "Clasificación: -"
            resultado_ckd.update()
            interpretacion_ckd.update()

    return ft.ExpansionPanelList(
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("CKD-EPI 2021", color=TEXT_COLOR),
                    subtitle=ft.Text("Estimación del filtrado glomerular (eGFR)",size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            sexo,
                            edad,
                            creatinina,
                            resultado_ckd,
                            interpretacion_ckd
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=5),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False
            )
        ]
    )



def calculadora_anion_gap():
    # Campos de entrada
    na_field = ft.TextField(
        label="Sodio (Na⁺) mEq/L",
        hint_text="Ej: 140",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    k_field = ft.TextField(
        label="Potasio (K⁺) mEq/L",
        hint_text="Ej: 4.0",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    cl_field = ft.TextField(
        label="Cloro (Cl⁻) mEq/L",
        hint_text="Ej: 100",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    hco3_field = ft.TextField(
        label="Bicarbonato (HCO₃⁻) mEq/L",
        hint_text="Ej: 24",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    resultado_texto = ft.Text(
        "Anion Gap: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    formula_text = ft.Text(
        "Fórmula usada: (Na⁺ + K⁺) - (Cl⁻ + HCO₃⁻)",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_anion_gap(e):
        try:
            na = float(na_field.value.replace(',', '.'))
            k = float(k_field.value.replace(',', '.'))
            cl = float(cl_field.value.replace(',', '.'))
            hco3 = float(hco3_field.value.replace(',', '.'))

            anion_gap = (na + k) - (cl + hco3)
            resultado_texto.value = f"Anion Gap: {anion_gap:.2f} mEq/L"
            formula_text.value = (f"Fórmula usada: ({na} + {k}) - ({cl} + {hco3}) = {anion_gap:.2f}")
        except ValueError:
            resultado_texto.value = "Anion Gap: Valor inválido"
            formula_text.value = "Fórmula usada: (Na⁺ + K⁺) - (Cl⁻ + HCO₃⁻)"

        resultado_texto.update()
        formula_text.update()

    na_field.on_change = calcular_anion_gap
    k_field.on_change = calcular_anion_gap
    cl_field.on_change = calcular_anion_gap
    hco3_field.on_change = calcular_anion_gap

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            na_field.value = ""
            k_field.value = ""
            cl_field.value = ""
            hco3_field.value = ""
            resultado_texto.value = "Anion Gap: -"
            formula_text.value = "Fórmula usada: (Na⁺ + K⁺) - (Cl⁻ + HCO₃⁻)"
            na_field.update()
            k_field.update()
            cl_field.update()
            hco3_field.update()
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
                    title=ft.Text("Anion Gap", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Column(
                                controls=[
                                    na_field,
                                    k_field,
                                    cl_field,
                                    hco3_field,
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

