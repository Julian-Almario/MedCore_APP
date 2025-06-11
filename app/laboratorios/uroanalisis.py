import flet as ft
from modules.colors import *

def orina_panel():
    datos_uroanalisis = {
        "Examen químico": {
            "Nitritos": "Negativo",
            "pH": "4.6 - 8.0 (media: 6.0)",
            "Proteínas": "<0.15 g /24 horas",
            "Glucosa": "Negativo",
            "Cetonas": "17 – 42 mg/dL",
            "Pigmentos biliares": "Negativo",
            "Urobilinógeno": "0.2 – 1.0 mg/dL",
            "Densidad": "1.016 - 1.022",
        },
        "Sedimento urinario": {
            "Leucocitos": "0 – 5 / campo de 40x",
            "Eritrocitos": "0 – 2 / campo de 40x",
            "Células epiteliales": "Cantidad variable",
            "Cilindros": "Hasta 2 hialinos / campo de 10x",
            "Cristales": "Cantidad variable",
        }
    }

    def crear_tabla(titulo, datos):
        return ft.Column(
            controls=[
                ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16, text_align=ft.TextAlign.CENTER),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(label=ft.Text("Parámetro", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(label=ft.Text("Valor normal", weight=ft.FontWeight.BOLD)),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(parametro)),
                                ft.DataCell(ft.Text(valor)),
                            ]
                        ) for parametro, valor in datos.items()
                    ],
                    column_spacing=40,
                    horizontal_margin=10,
                    divider_thickness=1
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    contenido = ft.Column(
        controls=[
            crear_tabla("Examen químico", datos_uroanalisis["Examen químico"]),
            crear_tabla("Sedimento urinario", datos_uroanalisis["Sedimento urinario"]),
        ],
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

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
                    title=ft.Text("Uroanálisis", color=TEXT_COLOR),
                    subtitle=ft.Text(
                        "Valores normales del examen químico y sedimento urinario",
                        size=SUBTITLE_SIZE,
                        color=TEXT_COLOR
                    ),
                ),
                content=ft.Container(
                    content=contenido,
                    padding=ft.padding.all(20)
                ),
                bgcolor=ft.Colors.BLUE_GREY_900,
                expanded=False
            )
        ]
    )
