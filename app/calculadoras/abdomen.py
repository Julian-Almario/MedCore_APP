import flet as ft
from modules.colors import *

def criterios_alvarado():
    criterios = [
        ("Dolor migratorio a fosa iliaca derecha", 1),
        ("Anorexia", 1),
        ("Náuseas o vómito", 1),
        ("Dolor en FID a la palpación", 2),
        ("Rebote positivo (Blumberg)", 1),
        ("Fiebre > 37.3 °C", 1),
        ("Leucocitosis > 10,000", 2),
        ("Desviación a la izquierda (neutrofilia)", 1)
    ]

    checkboxes = []

    resultado_texto = ft.Text(
        "Puntaje de Alvarado: -",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    interpretacion_texto = ft.Text(
        "",
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_alvarado(e=None):
        puntaje = sum(valor for cb, valor in checkboxes if cb.value)
        resultado_texto.value = f"Puntaje de Alvarado: {puntaje}"

        if puntaje <= 4:
            interpretacion = "Apendicitis poco probable"
            interpretacion_texto.color = "green"
        elif 5 <= puntaje <= 6:
            interpretacion = "Probabilidad compatible, observar"
            interpretacion_texto.color = "orange"
        elif 7 <= puntaje <= 8:
            interpretacion = "Probabilidad alta de apendicitis"
            interpretacion_texto.color = "red"
        else:  # 9 o 10
            interpretacion = "Apendicitis muy probable"
            interpretacion_texto.color = "red"

        interpretacion_texto.value = interpretacion
        resultado_texto.update()
        interpretacion_texto.update()

    def construir_tabla(criterios, checkboxes):
        filas = []
        for texto, valor in criterios:
            chk = ft.Checkbox(value=False, on_change=calcular_alvarado)
            checkboxes.append((chk, valor))
            fila = ft.Row(
                controls=[
                    ft.Container(ft.Text(texto, color=TEXT_COLOR), expand=True),
                    ft.Container(ft.Text(f"{valor:+}", color=TEXT_COLOR), width=30, alignment=ft.alignment.center_right),
                    ft.Container(chk, alignment=ft.alignment.center_right)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                height=32,
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
            resultado_texto.value = "Puntaje de Alvarado: -"
            interpretacion_texto.value = ""
            resultado_texto.update()
            interpretacion_texto.update()

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
                    title=ft.Text("Criterios de Alvarado para Apendicitis Aguda", color=TEXT_COLOR),
                    subtitle=ft.Text("Sospecha de apendicitis escala de alvarado", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            *construir_tabla(criterios, checkboxes),
                            ft.Divider(),
                            resultado_texto,
                            interpretacion_texto,
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=45),
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ]
    )
