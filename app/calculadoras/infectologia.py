import flet as ft
from modules.colors import *

def qsofa():
    check_frecuencia = ft.Checkbox(label="", value=False)
    check_presion = ft.Checkbox(label="", value=False)
    check_estado_mental = ft.Checkbox(label="", value=False)

    resultado_qsofa = ft.Text("Puntuación qSOFA: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_qsofa = ft.Text("Interpretación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_qsofa(e):
        puntos = 0
        if check_frecuencia.value:
            puntos += 1
        if check_presion.value:
            puntos += 1
        if check_estado_mental.value:
            puntos += 1

        resultado_qsofa.value = f"Puntuación qSOFA: {puntos}"

        if puntos >= 2:
            interpretacion = "Riesgo elevado de sepsis grave o muerte"
        else:
            interpretacion = "Riesgo bajo (seguir evaluando)"

        interpretacion_qsofa.value = f"Interpretación: {interpretacion}"

        resultado_qsofa.update()
        interpretacion_qsofa.update()

    check_frecuencia.on_change = calcular_qsofa
    check_presion.on_change = calcular_qsofa
    check_estado_mental.on_change = calcular_qsofa

    def fila_criterio(texto, checkbox):
        return ft.Row(
            controls=[
                ft.Text(texto, color=TEXT_COLOR,expand=True),
                checkbox
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

        if not is_expanded:
            check_frecuencia.value = False
            check_presion.value = False
            check_estado_mental.value = False
            resultado_qsofa.value = "Puntuación qSOFA: -"
            interpretacion_qsofa.value = "Interpretación: -"
            check_frecuencia.update()
            check_presion.update()
            check_estado_mental.update()
            resultado_qsofa.update()
            interpretacion_qsofa.update()

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
                    title=ft.Text("qSOFA (Sepsis)", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR),
                    subtitle=ft.Text("Probabilidad de Sepsis en urgencias", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            fila_criterio("Frecuencia respiratoria ≥ 22 rpm", check_frecuencia),
                            fila_criterio("Presión sistólica ≤ 100 mmHg", check_presion),
                            fila_criterio("Estado mental alterado (Glasgow < 15)", check_estado_mental),
                            resultado_qsofa,
                            interpretacion_qsofa
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=25
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=45),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )


def sofa_score():
    opciones_sofa = {
        "PaO₂/FiO₂": ["≥400", "300–399", "200–299 (sin VM)", "100–199 (con VM)", "<100 (con VM)"],
        "Plaquetas (x10³/µL)": ["≥150", "100–149", "50–99", "20–49", "<20"],
        "Glasgow Coma Scale": ["15", "13–14", "10–12", "6–9", "<6"],
        "Bilirrubina (mg/dL)": ["<1.2", "1.2–1.9", "2.0–5.9", "6.0–11.9", "≥12.0"],
        "Presión media / Vasopresores": [
            "No hipotensión",
            "MAP <70 mmHg",
            "Dopamina ≤5 o Dobutamina (cualquier dosis)",
            "Dopamina >5 o Nor/Epinefrina ≤0.1",
            "Dopamina >15 o Nor/Epinefrina >0.1"
        ],
        "Creatinina / diuresis": [
            "<1.2 mg/dL o diuresis normal",
            "1.2–1.9 mg/dL",
            "2.0–3.4 mg/dL",
            "3.5–4.9 mg/dL o diuresis <500 mL/día",
            "≥5.0 mg/dL o diuresis <200 mL/día"
        ]
    }

    selectores = {}
    for criterio in opciones_sofa:
        selectores[criterio] = ft.Dropdown(
            options=[ft.dropdown.Option(opcion) for opcion in opciones_sofa[criterio]],
            label=criterio,
            width=400
        )

    resultado_sofa = ft.Text("Puntuación SOFA: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_sofa = ft.Text("Interpretación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_sofa(e):
        puntuacion = 0
        for criterio, dropdown in selectores.items():
            indice = dropdown.options.index(next(opt for opt in dropdown.options if opt.key == dropdown.value)) if dropdown.value else 0
            puntuacion += indice

        resultado_sofa.value = f"Puntuación SOFA: {puntuacion}"

        if puntuacion >= 2:
            interpretacion = "Riesgo elevado de disfunción orgánica (evaluar sepsis)"
        else:
            interpretacion = "Riesgo bajo"

        interpretacion_sofa.value = f"Interpretación: {interpretacion}"
        resultado_sofa.update()
        interpretacion_sofa.update()

    for dropdown in selectores.values():
        dropdown.on_change = calcular_sofa

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            for d in selectores.values():
                d.value = None
                d.update()
            resultado_sofa.value = "Puntuación SOFA: -"
            interpretacion_sofa.value = "Interpretación: -"
            resultado_sofa.update()
            interpretacion_sofa.update()

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
                    title=ft.Text("SOFA Score (Sepsis)", color=TEXT_COLOR),
                    subtitle=ft.Text("Probabilidad de disfuncion organiza", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                    ),
                content=ft.Container(
                    content=ft.Column(
                        controls=list(selectores.values()) + [resultado_sofa, interpretacion_sofa],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )


def wifi_score():
    opciones_wifi = {
        "Herida (Wound)": [
            "Sin úlcera ni gangrena",
            "Úlcera superficial pequeña",
            "Úlcera profunda / gangrena limitada a dedos",
            "Úlcera extensa / gangrena extensa"
        ],
        "Isquemia (Ischemia) -- ITB ": [
            "≥0.8",
            "0.6-0.79",
            "0.4-0.59",
            "≤0.39"
        ],
        "Infección (Foot Infection)": [
            "Sin infección",
            "Infección superficial",
            "Infección profunda sin SRIS",
            "Infección con SRIS"
        ]
    }

    riesgo_amputacion = {
        0: {
            0: {0: "VL", 1: "VL", 2: "L", 3: "M"},
            1: {0: "VL", 1: "L",  2: "M", 3: "H"},
            2: {0: "L",  1: "M",  2: "H", 3: "H"},
            3: {0: "L",  1: "M",  2: "H", 3: "H"},
        },
        1: {
            0: {0: "VL", 1: "VL", 2: "L", 3: "M"},
            1: {0: "VL", 1: "L",  2: "M", 3: "H"},
            2: {0: "L",  1: "M",  2: "H", 3: "H"},
            3: {0: "M",  1: "M",  2: "H", 3: "H"},
        },
        2: {
            0: {0: "L",  1: "L",  2: "M", 3: "H"},
            1: {0: "M",  1: "M",  2: "H", 3: "H"},
            2: {0: "M",  1: "H",  2: "H", 3: "H"},
            3: {0: "H",  1: "H",  2: "H", 3: "H"},
        },
        3: {
            0: {0: "M",  1: "M",  2: "H", 3: "H"},
            1: {0: "H",  1: "H",  2: "H", 3: "H"},
            2: {0: "H",  1: "H",  2: "H", 3: "H"},
            3: {0: "H",  1: "H",  2: "H", 3: "H"},
        }
    }

    beneficio_revascularizacion = {
        0: {
            0: {0: "VL", 1: "VL", 2: "VL", 3: "VL"},
            1: {0: "VL", 1: "L",  2: "L",  3: "M"},
            2: {0: "L",  1: "L",  2: "M",  3: "M"},
            3: {0: "M",  1: "H",  2: "H",  3: "H"},
        },
        1: {
            0: {0: "VL", 1: "VL", 2: "VL", 3: "VL"},
            1: {0: "L",  1: "M",  2: "M",  3: "M"},
            2: {0: "M",  1: "H",  2: "H",  3: "H"},
            3: {0: "H",  1: "H",  2: "H",  3: "H"},
        },
        2: {
            0: {0: "VL", 1: "VL", 2: "VL", 3: "VL"},
            1: {0: "M",  1: "M",  2: "H",  3: "H"},
            2: {0: "H",  1: "H",  2: "H",  3: "H"},
            3: {0: "H",  1: "H",  2: "H",  3: "H"},
        },
        3: {
            0: {0: "VL", 1: "VL", 2: "VL", 3: "VL"},
            1: {0: "M",  1: "M",  2: "M",  3: "H"},
            2: {0: "H",  1: "H",  2: "H",  3: "H"},
            3: {0: "H",  1: "H",  2: "H",  3: "H"},
        }
    }

    texto = {"VL": "Muy bajo", "L": "Bajo", "M": "Moderado", "H": "Alto"}


    selectores = {}
    for criterio in opciones_wifi:
        selectores[criterio] = ft.Dropdown(
            label=criterio,
            width=450,
            options=[ft.dropdown.Option(op) for op in opciones_wifi[criterio]]
        )

    resultado = ft.Text("WIFI: -", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER)
    interpretacion = ft.Text("Resultado clínico: -", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER)

    def calcular_wifi(e):
        valores = []
        for d in selectores.values():
            if d.value:
                idx = d.options.index(next(o for o in d.options if o.key == d.value))
                valores.append(idx)
            else:
                valores.append(0)

        w, i, fi = valores
        riesgo = riesgo_amputacion[w][i][fi]
        beneficio = beneficio_revascularizacion[w][i][fi]

        resultado.value = f"WIFI: W{w}-I{i}-FI{fi}"
        interpretacion.value = (
            f"Riesgo de amputación a 1 año: {texto[riesgo]}\n"
            f"Beneficio de revascularización: {texto[beneficio]}"
        )

        resultado.update()
        interpretacion.update()

    for d in selectores.values():
        d.on_change = calcular_wifi

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        panel.bgcolor = SECONDARY_COLOR if panel.expanded else PRIMARY_COLOR
        panel.update()

        if not panel.expanded:
            for d in selectores.values():
                d.value = None
                d.update()
            resultado.value = "WIfI: -"
            interpretacion.value = "Resultado clínico: -"
            resultado.update()
            interpretacion.update()

    return ft.ExpansionPanelList(
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("WIFI Score (Pie diabético)", color=TEXT_COLOR),
                    subtitle=ft.Text(
                        "Riesgo de amputación y beneficio de revascularización",
                        size=SUBTITLE_SIZE,
                        color=TEXT_COLOR
                    )
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=list(selectores.values()) + [resultado, interpretacion],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

