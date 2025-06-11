import flet as ft
from modules.colors import *

def sodio_corregido():
    sodio = ft.TextField(label="Sodio sérico (mEq/L)", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    glucosa = ft.TextField(label="Glucosa (mg/dL)", keyboard_type=ft.KeyboardType.NUMBER, width=200)

    resultado_sodio = ft.Text("Sodio corregido: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    ecuacion_sodio = ft.Text("Ecuación: Na + 0.024 x (Glucosa - 100)", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR, size=SUBTITLE_SIZE)

    def calcular_sodio(e):
        try:
            na = float(sodio.value.replace(',', '.'))
            glu = float(glucosa.value.replace(',', '.'))

            sodio_corr = na + 0.016 * (glu - 100)
            sodio_corr = round(sodio_corr, 1)

            resultado_sodio.value = f"Sodio corregido: {sodio_corr} mEq/L"
            ecuacion_sodio.value = f"Ecuación: {na} + 0.024 x ({glu} - 100)"

        except Exception:
            resultado_sodio.value = "Sodio corregido: Datos inválidos"
            ecuacion_sodio.value = "Ecuación: Na + 0.016 x (Glucosa - 100)"

        resultado_sodio.update()
        ecuacion_sodio.update()

    for field in [sodio, glucosa]:
        field.on_change = calcular_sodio

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            sodio.value = ""
            glucosa.value = ""
            for field in [sodio, glucosa]:
                field.update()
            resultado_sodio.value = "Sodio corregido: -"
            ecuacion_sodio.value = "Ecuación: Na + 0.024 x (Glucosa - 100)"
            resultado_sodio.update()
            ecuacion_sodio.update()

    return ft.ExpansionPanelList(
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Sodio corregido", color=TEXT_COLOR),
                    subtitle=ft.Text("Ajuste del sodio sérico por hiperglucemia", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            sodio,
                            glucosa,
                            resultado_sodio,
                            ecuacion_sodio,
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False
            )
        ]
    )