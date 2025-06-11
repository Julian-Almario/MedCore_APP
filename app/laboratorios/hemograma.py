import flet as ft
from modules.colors import *

def hemograma_panel():
    rangos_por_edad = {
        "Neonatos": {
            "Parto": {
                "Hemoglobina (g/dL)": "16.5-13.5",
                "Hematocrito (%)": "55-42",
                "Hematíes (millones/µL)": "4.7-3.9",
                "VCM (fL)": "108-98",
                "HCM (pg)": "34-31",
                "CHCM (g/dL)": "33-30",
                "Reticulocitos (%)": "3.2-1.8",
                "Leucocitos totales (10^3/µL)": "9.3",
                "Neutrófilos (%)": "41-81",
                "Linfocitos (%)": "2-11",
                "Monocitos (%)": "26-36",
                "Eosinófilos (%)": "0.1"
            },
            "1-3 días": {
                "Hemoglobina (g/dL)": "18.5-13.5",
                "Hematocrito (%)": "55-45",
                "Hematíes (millones/µL)": "5.3-4.0",
                "VCM (fL)": "108-94",
                "HCM (pg)": "34-31",
                "CHCM (g/dL)": "33-30",
                "Reticulocitos (%)": "3.0-1.6",
                "Leucocitos totales (10^3/µL)": "11",
                "Neutrófilos (%)": "7.8-14.5",
                "Linfocitos (%)": "4.2",
                "Monocitos (%)": "0.6",
                "Eosinófilos (%)": "0.1"
            },
            "1 semana": {
                "Hemoglobina (g/dL)": "17.5-13.5",
                "Hematocrito (%)": "54-42",
                "Hematíes (millones/µL)": "5.1-3.9",
                "VCM (fL)": "107-88",
                "HCM (pg)": "34-28",
                "CHCM (g/dL)": "33-28",
                "Reticulocitos (%)": "0.5-0.1",
                "Leucocitos totales (10^3/µL)": "10",
                "Neutrófilos (%)": "1.5-15",
                "Linfocitos (%)": "2-17",
                "Monocitos (%)": "31-51",
                "Eosinófilos (%)": "0.1"
            },
            "1 mes": {
                "Hemoglobina (g/dL)": "14.0-10.0",
                "Hematocrito (%)": "43-31",
                "Hematíes (millones/µL)": "4.1-3.1",
                "VCM (fL)": "102-86",
                "HCM (pg)": "31-26",
                "CHCM (g/dL)": "31-28",
                "Reticulocitos (%)": "0.8-0.1",
                "Leucocitos totales (10^3/µL)": "5-20",
                "Neutrófilos (%)": "1.0-10.0",
                "Linfocitos (%)": "22-55",
                "Monocitos (%)": "33-50",
                "Eosinófilos (%)": "0.3"
            },
            "2-6 meses": {
                "Hemoglobina (g/dL)": "12.5–11.5",
                "Hematocrito (%)": "37–33",
                "Hematíes (millones/µL)": "3.6–3.2",
                "VCM (fL)": "95–78",
                "HCM (pg)": "29–24",
                "CHCM (g/dL)": "31–27",
                "Reticulocitos (%)": "1.0–0.2",
                "Leucocitos totales (10^3/µL)": "5.5–18",
                "Neutrófilos (%)": "2.0–20.0",
                "Linfocitos (%)": "10.0–50.0",
                "Monocitos (%)": "44–47",
                "Eosinófilos (%)": "0.3"
            }
        },
        "Niños": {
            "6-12 años": {
                "Hemoglobina (g/dL)": "13.5–11.5",
                "Hematocrito (%)": "42–35",
                "VCM (fL)": "86–75",
                "HCM (pg)": "28–24",
                "CHCM (g/dL)": "32–27",
                "Reticulocitos (%)": "1.0–0.2",
                "Leucocitos totales (10^3/µL)": "7.5",
                "Neutrófilos (%)": "38–54",
                "Linfocitos (%)": "25–45",
                "Monocitos (%)": "3",
                "Eosinófilos (%)": "3"
            }
        },
        "Adultos": {
            "Adulto (varón)": {
                "Hemoglobina (g/dL)": "15.5–13.5",
                "Hematocrito (%)": "47–41",
                "VCM (fL)": "90–80",
                "HCM (pg)": "30–26",
                "CHCM (g/dL)": "34–31",
                "Reticulocitos (%)": "1.0–0.2",
                "Leucocitos totales (10^3/µL)": "7.4",
                "Neutrófilos (%)": "42–72",
                "Linfocitos (%)": "15–48",
                "Monocitos (%)": "3",
                "Eosinófilos (%)": "3"
            },
            "Adulto (mujer)": {
                "Hemoglobina (g/dL)": "14.0–12.0",
                "Hematocrito (%)": "41–36",
                "VCM (fL)": "90–80",
                "HCM (pg)": "30–26",
                "CHCM (g/dL)": "34–31",
                "Reticulocitos (%)": "1.0–0.2",
                "Leucocitos totales (10^3/µL)": "7.4",
                "Neutrófilos (%)": "42–72",
                "Linfocitos (%)": "15–48",
                "Monocitos (%)": "3",
                "Eosinófilos (%)": "3"
            }
        }
    }

    grupo_selector = ft.Dropdown(
        label="Selecciona grupo etario",
        options=[
            ft.dropdown.Option("Neonatos"),
            ft.dropdown.Option("Niños"),
            ft.dropdown.Option("Adultos")
        ],
        value="",
        width=300
    )

    edad_selector = ft.Dropdown(label="Selecciona edad", width=300, value="")

    hemograma_datos = ft.Column(spacing=10)

    def actualizar_edades(e):
        grupo = grupo_selector.value
        if not grupo or grupo not in rangos_por_edad:
            edad_selector.options = []
            edad_selector.value = None
            edad_selector.update()
            actualizar_hemograma(None)
            return
        edad_selector.options = [
            ft.dropdown.Option(edad) for edad in rangos_por_edad[grupo]
        ]
        if grupo == "Neonatos":
            edad_selector.value = "Parto"
        else:
            edad_selector.value = edad_selector.options[0].key if edad_selector.options else None
        edad_selector.update()
        actualizar_hemograma(None)

    def actualizar_hemograma(e):
        grupo = grupo_selector.value
        edad = edad_selector.value
        hemograma_datos.controls.clear()
        if grupo and grupo in rangos_por_edad and edad and edad in rangos_por_edad[grupo]:
            for parametro, valor in rangos_por_edad[grupo][edad].items():
                hemograma_datos.controls.append(
                    ft.Row(
                        controls=[
                            ft.Text(parametro, width=200),
                            ft.Text(valor, width=100)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
        hemograma_datos.update()
        grupo_selector.update()
        edad_selector.update()

    grupo_selector.on_change = actualizar_edades
    edad_selector.on_change = actualizar_hemograma

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

        if not is_expanded:
            grupo_selector.value = None
            edad_selector.options = []
            edad_selector.value = None
            hemograma_datos.controls.clear()
            grupo_selector.update()
            edad_selector.update()
            hemograma_datos.update()

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
                    title=ft.Text("Hemograma", text_align=ft.TextAlign.LEFT, color=TEXT_COLOR),
                    subtitle=ft.Text("Valores normales Neonatos > Adultos", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            grupo_selector,
                            edad_selector,
                            hemograma_datos
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