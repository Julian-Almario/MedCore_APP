import flet as ft
from modules.colors import *

def flujo_vaginal_panel():
    datos_flujo_vaginal = {
        "Microscopía en fresco": {
            "Leucocitos": "0 - 10 por campo",
            "Células epiteliales": "Presencia normal",
            "Clue cells": "Ausentes",
            "Células guía (hifas de Candida)": "Ausentes",
            "Trichomonas vaginalis": "Ausente",
            "Lactobacilos": "Presentes (flora normal)",
            "pH vaginal": "3.8 - 4.5",
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
            crear_tabla("Microscopía en fresco", datos_flujo_vaginal["Microscopía en fresco"]),
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
                    title=ft.Text("Flujo vaginal", color=TEXT_COLOR),
                    subtitle=ft.Text(
                        "Valores normales de la microscopía del flujo vaginal",
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

def vaginitis_panel():
    datos_vaginitis = [
        {
            "condicion": "Normal",
            "sintomas": "Ninguno",
            "flujo": "Blanco, claro",
            "koh": "-",
            "ph": "3.8 - 4.2",
            "microscopico": "NA"
        },
        {
            "condicion": "Vaginosis bacteriana",
            "sintomas": "Mal olor, aumenta luego de coito o menstruación",
            "flujo": "Líquido, gris o blanco, adherente, usualmente abundante",
            "koh": "+",
            "ph": ">4.5",
            "microscopico": "Células guía, acúmulos bacterianos"
        },
        {
            "condicion": "Vulvovaginitis candidiásica",
            "sintomas": "Prurito, ardor, descarga",
            "flujo": "Blanco, grumoso",
            "koh": "-",
            "ph": "<4.5",
            "microscopico": "Hifas, seudohifas, micelios"
        },
        {
            "condicion": "Tricomoniasis",
            "sintomas": "Mal olor, disuria, prurito, spotting",
            "flujo": "Amarillo-verde, espumoso, adherente, abundante",
            "koh": "±",
            "ph": ">4.5",
            "microscopico": "Trichomonas"
        },
        {
            "condicion": "Vaginitis aeróbica",
            "sintomas": "Mal olor, prurito",
            "flujo": "Líquido, purulento",
            "koh": "-",
            "ph": ">4.5",
            "microscopico": "Leucocitos abundantes, aerobios"
        },
        {
            "condicion": "Vaginosis citolítica",
            "sintomas": "Prurito, ardor, fase lútea",
            "flujo": "Blanco, cremoso, no fétido",
            "koh": "-",
            "ph": "3.5 – 4.5",
            "microscopico": "Lactobacilos abundantes, lisis células epiteliales"
        }
    ]

    def tarjeta_vaginitis(fila):
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.all(15),
                content=ft.Column([
                    ft.Text(fila["condicion"], size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"• Síntomas: {fila['sintomas']}"),
                    ft.Text(f"• Flujo: {fila['flujo']}"),
                    ft.Text(f"• Prueba KOH: {fila['koh']}"),
                    ft.Text(f"• pH: {fila['ph']}"),
                    ft.Text(f"• Hallazgos microscópicos: {fila['microscopico']}"),
                ],
                spacing=5
                )
            ),
            elevation=3,
            margin=10,
            width=500,
        )

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

    tarjetas = ft.Column(
        controls=[tarjeta_vaginitis(fila) for fila in datos_vaginitis],
        width=True,
        spacing=10,
    )

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
                    title=ft.Text("Panel de vaginitis", color=TEXT_COLOR),
                    subtitle=ft.Text(
                        "Síntomas, características del flujo y hallazgos microscópicos",
                        size=SUBTITLE_SIZE,
                        color=TEXT_COLOR
                    ),
                ),
                content=ft.Container(
                    content=tarjetas,
                    padding=ft.padding.all(10)
                ),
                bgcolor=ft.Colors.BLUE_GREY_900,
                expanded=False
            )
        ]
    )
