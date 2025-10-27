
# Pagian de algoritmos
    #Ruta de almacenamiento de algoritmos
    RUTA_ALGO = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage", "data", "algoritmos"))
    os.makedirs(RUTA_ALGO, exist_ok=True) #Confirmacion de que exista el .json

    #Extensiones de imagenes validas
    EXTENSIONES_VALIDAS = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"]

    def es_imagen_valida(ruta_imagen):
        return os.path.exists(ruta_imagen) and os.path.splitext(ruta_imagen)[1].lower() in EXTENSIONES_VALIDAS

    def cargar_algoritmos_desde_json(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return [crear_panel_algoritmo(algo) for algo in datos]

    def crear_panel_algoritmo(algo: dict):
        panel_ref = ft.Ref[ft.ExpansionPanel]()

        def on_expand_change(e):
            panel = panel_ref.current
            is_expanded = panel.expanded
            panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
            panel.update()

        ruta_imagen = os.path.join(RUTA_ALGO, algo["imagen"])

        if not es_imagen_valida(ruta_imagen):
            imagen_componente = ft.Text(
                f"Imagen no encontrada o formato no soportado: {algo['imagen']}",
                color=ft.Colors.RED,
                selectable=True
            )
        else:
            imagen_componente = ft.InteractiveViewer(
                min_scale=0.5,
                max_scale=5,
                boundary_margin=ft.margin.all(20),
                content=ft.Image(
                    src=ruta_imagen,
                    fit=ft.ImageFit.CONTAIN,
                    width=600,
                    height=400,
                    expand=True
                )
            )

        #INformacion presentada en las pestañas de la lista
        return {
            "titulo": algo["nombre"],
            "tags": algo["tags"],
            "componente": ft.ExpansionPanelList(
                on_change=on_expand_change,
                expand_icon_color=TEXT_COLOR,
                elevation=8,
                divider_color=TEXT_COLOR,
                controls=[
                    ft.ExpansionPanel(
                        ref=panel_ref,
                        header=ft.ListTile(
                            title=ft.Text(algo["nombre"], text_align=ft.TextAlign.LEFT),
                        ),
                        content=ft.Container(
                            content=imagen_componente,
                            padding=15,
                        ),
                        bgcolor=PRIMARY_COLOR,
                        expanded=False,
                    )
                ],
            )
        }

    #Paginacion global de los algoritmos
    def pagina_algoritmos(page: ft.Page):
        list_data = cargar_algoritmos_desde_json(os.path.join(RUTA_ALGO, "algoritmos.json"))
        buscar = "Buscar algoritmos..."

        mensaje_no_resultados = ft.Text(
            value="No se encontraron algoritmos.",
            style=ft.TextThemeStyle.BODY_MEDIUM,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        list_container, filtrar_items = list_content_search(list_data, mensaje_no_resultados)

        return ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    content=search_bar(filtrar_items, buscar),
                    padding=ft.padding.symmetric(horizontal=40, vertical=10),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        controls=[list_container],
                    ),
                ),
            ],
        )
