import flet as ft
from modules.colors import *

def lcr_panel():
    valores_normales_lcr = {
        "Recién nacido (RN)": {
            "Presión de apertura (cmH₂O)": "8–11",
            "Aspecto": "Claro",
            "Color": "Incoloro",
            "Glucosa (mg/dL)": "40–80",
            "Proteínas (mg/dL)": "20–120",
            "Células (células/mm³)": "0–30 (principalmente mononucleares)",
            "Lactato (mmol/L)": "<3.5"
        },
        "Lactante (>1 mes)": {
            "Presión de apertura (cmH₂O)": "10–18",
            "Aspecto": "Claro",
            "Color": "Incoloro",
            "Glucosa (mg/dL)": "40–80",
            "Proteínas (mg/dL)": "15–45",
            "Células (células/mm³)": "0–10",
            "Lactato (mmol/L)": "<2.1"
        },
        "Niño mayor / Adolescente": {
            "Presión de apertura (cmH₂O)": "10–20",
            "Aspecto": "Claro",
            "Color": "Incoloro",
            "Glucosa (mg/dL)": "45–80 (≈ 60% de la glucemia)",
            "Proteínas (mg/dL)": "15–45",
            "Células (células/mm³)": "0–5",
            "Lactato (mmol/L)": "<2.1"
        },
        "Adulto": {
            "Presión de apertura (cmH₂O)": "10–20",
            "Aspecto": "Claro",
            "Color": "Incoloro",
            "Glucosa (mg/dL)": "45–80 (≈ 60% de la glucemia)",
            "Proteínas (mg/dL)": "15–45",
            "Células (células/mm³)": "0–5",
            "Lactato (mmol/L)": "1.2–2.1"
        }
    }

    edad_selector = ft.Dropdown(
        label="Selecciona grupo etario",
        options=[ft.dropdown.Option(k) for k in valores_normales_lcr.keys()],
        width=300,
    )

    lcr_datos = ft.Column(spacing=8)

    def actualizar_lcr(e):
        grupo = edad_selector.value
        lcr_datos.controls.clear()
        if grupo and grupo in valores_normales_lcr:
            for parametro, valor in valores_normales_lcr[grupo].items():
                lcr_datos.controls.append(
                    ft.Row(
                        controls=[
                            ft.Text(f"{parametro}:", width=250),
                            ft.Text(valor, width=150)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
        lcr_datos.update()

    edad_selector.on_change = actualizar_lcr

    # Tabla Score de Boyer
    boyer_score_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Variable", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("0", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("1", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("2", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("Temperatura")), ft.DataCell(ft.Text("< 39,5°C")), ft.DataCell(ft.Text("> 39,5°C")), ft.DataCell(ft.Text("-"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Petequias")), ft.DataCell(ft.Text("Ausentes")), ft.DataCell(ft.Text("-")), ft.DataCell(ft.Text("Presentes"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Signos meníngeos")), ft.DataCell(ft.Text("Ausentes")), ft.DataCell(ft.Text("Presentes")), ft.DataCell(ft.Text("-"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Proteínas LCR (g/dL)")), ft.DataCell(ft.Text("< 0,9")), ft.DataCell(ft.Text("0,9–1,4")), ft.DataCell(ft.Text("> 1,4"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Glucosa LCR (mg/dL)")), ft.DataCell(ft.Text("> 35")), ft.DataCell(ft.Text("35–20")), ft.DataCell(ft.Text("< 20"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Leucocitos LCR")), ft.DataCell(ft.Text("< 1.000")), ft.DataCell(ft.Text("1.000–4.000")), ft.DataCell(ft.Text("> 4.000"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("PMN LCR, %")), ft.DataCell(ft.Text("< 60")), ft.DataCell(ft.Text("> 60")), ft.DataCell(ft.Text("-"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Leucocitos en sangre")), ft.DataCell(ft.Text("< 15.000")), ft.DataCell(ft.Text("> 15.000")), ft.DataCell(ft.Text("-"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Cayados en sangre, %")), ft.DataCell(ft.Text("< 6")), ft.DataCell(ft.Text("6–14")), ft.DataCell(ft.Text("> 15"))]),
        ],
        divider_thickness=1
    )

    recomendaciones_boyer = ft.Container(
        content=ft.Text(
            "> Interpretación del Score de Boyer\n"
            "- > 5 puntos: Iniciar antibiótico.\n"
            "- 3–4 puntos: Evaluar estado general y considerar antibiótico.\n"
            "- < 2 puntos: No iniciar antibiótico.\n\n"
            "> Excepciones al uso del score:\n"
            "- < 3 meses de edad\n"
            "- Paciente clínicamente inestable\n"
            "- Uso previo de antibióticos\n"
            "- Factores de riesgo: válvula de derivación, TCE, neurocirugía, mielomeningocele, quemaduras, inmunodepresión",
            selectable=True,
            text_align=ft.TextAlign.LEFT,
        ),
        padding=10,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_radius=8
    )

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        
        if not panel_ref.current.expanded:
            edad_selector.value = None
            lcr_datos.controls.clear()
            edad_selector.update()
            lcr_datos.update()

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
                    title=ft.Text("Líquido Cefalorraquídeo (LCR)", color=TEXT_COLOR),
                    subtitle=ft.Text("LCR valores normales y Boyer score", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(content=edad_selector, padding=ft.padding.only(bottom=10)),
                            lcr_datos,
                            ft.Divider(thickness=2),
                            ft.Text("Score de Boyer para meningitis bacteriana", weight=ft.FontWeight.BOLD, size=16),
                            boyer_score_table,
                            recomendaciones_boyer,
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(20)
                ),
                bgcolor=ft.Colors.BLUE_GREY_900,
                expanded=False
            )
        ]
    )

