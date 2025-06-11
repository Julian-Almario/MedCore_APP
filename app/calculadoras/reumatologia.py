import flet as ft
from modules.colors import *

def slicc_page():
    criterios_clinicos = [
        "Lupus cutáneo agudo",
        "Lupus cutáneo crónico",
        "Úlceras orales o nasales",
        "Alopecia no cicatricial",
        "Artritis",
        "Serositis (pleuritis o pericarditis)",
        "Nefritis lúpica",
        "Alteración neurológica (convulsiones o psicosis)",
        "Anemia hemolítica",
        "Leucopenia (< 4000) o linfopenia (< 1000)",
        "Trombocitopenia (< 100,000)"
    ]

    criterios_inmunologicos = [
        "ANA positivo",
        "Anti-DNA positivo",
        "Anti-Sm positivo",
        "Antifosfolípidos positivos",
        "Disminución de C3 y/o C4",
        "Prueba de Coombs directa positiva (sin anemia hemolítica)"
    ]

    resultado = ft.Text(
        "Selecciona criterios para evaluar diagnóstico.",
        size=14,
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        text_align=ft.TextAlign.CENTER,
        color=TEXT_COLOR,
    )

    checks_clinicos = []
    checks_inmuno = []

    def evaluar(e=None):
        count_clinicos = sum(1 for c in checks_clinicos if c.value)
        count_inmuno = sum(1 for c in checks_inmuno if c.value)
        total = count_clinicos + count_inmuno

        tiene_nefritis = checks_clinicos[6].value
        ana_positivo = checks_inmuno[0].value
        anti_dna = checks_inmuno[1].value

        if total >= 4 and count_clinicos >= 1 and count_inmuno >= 1:
            resultado.value = (
                f"Diagnóstico posible de LES (criterios ≥4).\n"
                f"Total: {total}, Clínicos: {count_clinicos}, Inmunológicos: {count_inmuno}"
            )
            resultado.color = "green"
        elif tiene_nefritis and (ana_positivo or anti_dna):
            resultado.value = (
                f"Diagnóstico posible de LES (nefritis lúpica + ANA o Anti-DNA positivo).\n"
                f"Total: {total}, Clínicos: {count_clinicos}, Inmunológicos: {count_inmuno}"
            )
            resultado.color = "green"
        else:
            resultado.value = (
                f"No cumple criterios diagnósticos.\n"
                f"Total: {total}, Clínicos: {count_clinicos}, Inmunológicos: {count_inmuno}"
            )
            resultado.color = "red"

        resultado.update()

    def construir_tabla(criterios, checkboxes):
        filas = []
        for texto in criterios:
            chk = ft.Checkbox(value=False, on_change=evaluar)
            checkboxes.append(chk)
            fila = ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(
                            texto,
                            color=TEXT_COLOR,
                            size=14,
                            weight=ft.FontWeight.NORMAL,
                        ),
                        expand=True,
                    ),
                    ft.Container(chk, alignment=ft.alignment.center_right)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
            for c in checks_clinicos + checks_inmuno:
                c.value = False
                c.update()
            resultado.value = "Selecciona criterios para evaluar diagnóstico."
            resultado.color = TEXT_COLOR
            resultado.update()

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
                    title=ft.Text(
                        "Criterios SLICC para diagnóstico de LES",
                        color=TEXT_COLOR,
                        size=16,
                        style=ft.TextThemeStyle.TITLE_MEDIUM,
                    ),
                    subtitle=ft.Text("Criterios de clasificación de LES", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Criterios clínicos",
                                style=ft.TextThemeStyle.TITLE_MEDIUM,
                                size=15,
                                color=TEXT_COLOR,
                                ),
                            *construir_tabla(criterios_clinicos, checks_clinicos),
                            ft.Divider(),
                            ft.Text(
                                "Criterios inmunológicos",
                                style=ft.TextThemeStyle.TITLE_MEDIUM,
                                size=15,
                                color=TEXT_COLOR,
                            ),
                            *construir_tabla(criterios_inmunologicos, checks_inmuno),
                            ft.Divider(),
                            resultado,
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(vertical=12, horizontal=45),
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ]
    )
