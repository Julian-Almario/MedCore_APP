import flet as ft
from  modules.colors import *

def imc():
    peso_field = ft.TextField(
        label="Peso (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )

    talla_field = ft.TextField(
        label="Talla (m)",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )

    resultado_imc = ft.Text("IMC: -")
    categoria_imc = ft.Text("Categoría: -")

    def calcular_imc(e):
        try:
            peso = float(peso_field.value)
            talla = float(talla_field.value)
            imc_valor = peso / (talla ** 2)
            resultado_imc.value = f"IMC: {imc_valor:.2f}"

            # Clasificación según valor
            if imc_valor < 18.5:
                categoria = "Bajo peso"
            elif 18.5 <= imc_valor <= 24.9:
                categoria = "Normal"
            elif 25.0 <= imc_valor <= 29.9:
                categoria = "Sobrepeso"
            else:
                categoria = "Obesidad"

            categoria_imc.value = f"Categoría: {categoria}"
        except (ValueError, ZeroDivisionError):
            resultado_imc.value = "IMC: Valor inválido"
            categoria_imc.value = "Categoría: -"
        resultado_imc.update()
        categoria_imc.update()

    # Eventos de cambio
    peso_field.on_change = calcular_imc
    talla_field.on_change = calcular_imc

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            peso_field.value = ""
            talla_field.value = ""
            resultado_imc.value = "IMC: -"
            categoria_imc.value = "Categoría: -"
            peso_field.update()
            talla_field.update()
            resultado_imc.update()
            categoria_imc.update()


    return ft.ExpansionPanelList(
        ref=panel_list_ref,
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(title=ft.Text("IMC"),text_color=TEXT_COLOR),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            peso_field,
                            talla_field,
                            resultado_imc,
                            categoria_imc
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.symmetric(vertical=25),
                ),
                bgcolor=ft.Colors.BLUE_GREY_900,
                expanded=False,
            )
        ],
    )

def talla_medioparental():
    tallapadre_field = ft.TextField(
        label="Talla del padre (cm)",
        hint_text="Ej: 170",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    tallamadre_field = ft.TextField(
        label="Talla de la madre (cm)",
        hint_text="Ej: 160",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=250
    )

    k_selector = ft.Dropdown(
        label="Sexo del paciente",
        options=[
            ft.dropdown.Option("Niño k = +6.5cm"),
            ft.dropdown.Option("Niña k = -6.5cm")
        ],
        value="Niño k = +6.5cm",
        width=250
    )

    resultado_texto = ft.Text(
        "Talla medioparental estimada",
        style=ft.TextThemeStyle.HEADLINE_SMALL,
        color=TEXT_COLOR,
        text_align=ft.TextAlign.CENTER
    )

    formula_text = ft.Text(
        "Fórmula usada: ((Talla madre + Talla padre) / 2) ± 6.5 cm",
        color=TEXT_COLOR,
        size=14,
        text_align=ft.TextAlign.CENTER
    )

    def calcular_talla(e):
        try:
            talla_padre = float(tallapadre_field.value)
            talla_madre = float(tallamadre_field.value)
            k = 6.5 if "Niño" in k_selector.value else -6.5

            talla_mp = ((talla_padre + talla_madre) / 2) + k
            resultado_texto.value = f"Talla estimada: {talla_mp:.1f} cm"
            formula_text.value = (
                f"Fórmula usada: (({talla_padre} + {talla_madre}) / 2) {'+' if k > 0 else '-'} 6.5 = {talla_mp:.1f} cm"
            )
        except ValueError:
            resultado_texto.value = "Talla estimada: Valor inválido"
            formula_text.value = "Fórmula usada: ((Talla madre + Talla padre) / 2) ± 6.5 cm"

        resultado_texto.update()
        formula_text.update()

    tallapadre_field.on_change = calcular_talla
    tallamadre_field.on_change = calcular_talla
    k_selector.on_change = calcular_talla

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            tallapadre_field.value = ""
            tallamadre_field.value = ""
            k_selector.value = "Niño k = +6.5cm"
            resultado_texto.value = "Talla medioparental estimada"
            formula_text.value = "Fórmula usada: ((Talla madre + Talla padre) / 2) ± 6.5 cm"
            tallapadre_field.update()
            tallamadre_field.update()
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
                    title=ft.Text("Talla medioparental", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([formula_text], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column(
                                controls=[
                                    tallapadre_field,
                                    tallamadre_field,
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