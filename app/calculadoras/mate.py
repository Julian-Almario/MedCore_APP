import flet as ft
from modules.colors import *

def regla_de_tres():
    a_field = ft.TextField(hint_text="A", keyboard_type=ft.KeyboardType.NUMBER, width=80, text_align=ft.TextAlign.CENTER)
    b_field = ft.TextField(hint_text="B", keyboard_type=ft.KeyboardType.NUMBER, width=80, text_align=ft.TextAlign.CENTER)
    y_field = ft.TextField(hint_text="Y", keyboard_type=ft.KeyboardType.NUMBER, width=80, text_align=ft.TextAlign.CENTER)

    resultado_x = ft.Text("X", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, size=20, text_align=ft.TextAlign.CENTER)
    enter = ft.Text("", weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER, size=0, text_align=ft.TextAlign.CENTER)
    formula_text = ft.Text("Fórmula usada: X = (Y x B) / A", color=TEXT_COLOR, size=14, text_align=ft.TextAlign.CENTER)
    resultado_valor = ft.Text("X: -", style=ft.TextThemeStyle.HEADLINE_SMALL, color=TEXT_COLOR, text_align=ft.TextAlign.CENTER)

    def calcular_regla_de_tres(e):
        try:
            if not all([a_field.value, b_field.value, y_field.value]):
                raise Exception

            a = float(a_field.value)
            if a == 0:
                raise Exception

            b = float(b_field.value)
            y = float(y_field.value)
            x = (y * b) / a

            resultado_x.value = f"{x:.2f}"
            resultado_valor.value = f"X: {x:.2f}"
            formula_text.value = f"Fórmula usada: X = ({y} x {b}) / {a} = {x:.2f}"
        except:
            resultado_x.value = "X"
            resultado_valor.value = "X: Valor inválido"
            formula_text.value = "Fórmula usada: X = (Y x B) / A"
        finally:
            for control in [resultado_x, resultado_valor, formula_text]:
                try:
                    if control.page:
                        control.update()
                except:
                    pass

    a_field.on_change = calcular_regla_de_tres
    b_field.on_change = calcular_regla_de_tres
    y_field.on_change = calcular_regla_de_tres

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        try:
            panel.update()
        except:
            pass

        if not is_expanded:
            a_field.value = ""
            b_field.value = ""
            y_field.value = ""
            resultado_x.value = "X"
            resultado_valor.value = "X: -"
            formula_text.value = "Fórmula usada: X = (Y × B) / A"
            for control in [a_field, b_field, y_field, resultado_x, resultado_valor, formula_text]:
                try:
                    if control.page:
                        control.update()
                except:
                    pass

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
                    title=ft.Text("Regla de tres (Directa)", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([formula_text], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row(
                                controls=[
                                    ft.Column([a_field, b_field], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                                    ft.Container(content=ft.Text(" = ", size=25, color=TEXT_COLOR), alignment=ft.alignment.center),
                                    ft.Column([y_field, enter, resultado_x], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.only(bottom=25)
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

