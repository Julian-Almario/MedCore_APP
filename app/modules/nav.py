import flet as ft


def nav(page, page_change):
    drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        selected_index=0,
        on_change=page_change,
        controls=[
            ft.Container(width=10, height=10),
            ft.NavigationDrawerDestination(
                label="Home",
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.HOME),
            ),
            ft.Divider(thickness=1),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.FORMAT_LIST_BULLETED_OUTLINED),
                label="Medicamentos",
                selected_icon=ft.Icons.FORMAT_LIST_BULLETED,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.CALCULATE_OUTLINED),
                label="Calculadoras",
                selected_icon=ft.Icons.CALCULATE,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED),
                label="Laboratorios",
                selected_icon=ft.Icons.ASSIGNMENT_SHARP,
            ),
                ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED),
                label="Historias clinica",
                selected_icon=ft.Icons.ASSIGNMENT_SHARP,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED),
                label="Informacion",
                selected_icon=ft.Icons.ASSIGNMENT_SHARP,
            ),
        ],
    )

    bar = ft.AppBar(
        leading=ft.Container(content=ft.Icon(ft.Icons.MEDICAL_SERVICES), padding=ft.padding.only(left=12)),
        leading_width=30,
        title=ft.Text("MedCore"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.Container(content=ft.Row(
        controls=[
            ft.IconButton(
                width=40,
                height=40,
                style=ft.ButtonStyle(bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                content=ft.Row(
                   [ft.Icon(name=ft.Icons.FORMAT_LIST_BULLETED, color=ft.Colors.WHITE)],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND),
                on_click=lambda e: page.open(drawer)
            )
        ],
        alignment=ft.MainAxisAlignment.END
    ), padding=ft.padding.only(right=12))
        ]
    )
    return bar, drawer

def search_bar(filtrar, buscar):
    return ft.TextField(
        label=buscar,
        on_change=filtrar,
        border=ft.InputBorder.UNDERLINE,
        border_color=ft.Colors.OUTLINE,
        bgcolor=ft.Colors.TRANSPARENT,
        filled=False,
        dense=True,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
        width=400,
        expand=True,
    )

def list_content_search(list_content):
    list_content.sort(key=lambda x: x["titulo"].lower())

    list_container = ft.Column(spacing=20)
    buscar = "Buscar..."

    def build_list(filtered_items):
        list_container.controls.clear()
        for cont in filtered_items:
            list_container.controls.append(cont["componente"])
        list_container.update()

    def filtrar_calculadoras(e):
        filtro = e.control.value.lower()
        filtered_items = []
        for cont in list_content:
            titulo = cont["titulo"].lower()
            tags = " ".join(cont["tags"]).lower()
            if filtro in titulo or filtro in tags:
                filtered_items.append(cont)
        build_list(filtered_items)

    for cont in list_content:
        list_container.controls.append(cont["componente"])

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(
                content=search_bar(filtrar_calculadoras, buscar),
                padding=ft.padding.symmetric(horizontal=40)
            ),
            ft.Container(
                content=list_container,
                padding=ft.padding.symmetric(horizontal=40)
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )