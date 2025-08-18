import flet as ft

def info_page(page: ft.Page):

    def web(e):
        page.launch_url("https://www.julianalmario.social/")

    my_web = ft.GestureDetector(
        content=ft.Image(src="../assets/myweb.png", width=150, height=50),
        on_tap=web,
    )

    images_row = ft.Row(
        controls=[my_web],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )
    
    #Informacion del desarrollo
    creador_info = ft.Column(
        controls=[
            ft.Text("Created by Julian Almario Loaiza", size=18),
            images_row,
            ft.Text("Versión: 0.2.0 (Agosto 2025)", size=14, color=ft.Colors.OUTLINE),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    #Lista de referencias
    referencias = [
        "- Huerta Aragonés J, Cela de Julián E. Hematología práctica: interpretación del hemograma y de las pruebas de coagulación. En: AEPap (ed.). Curso de Actualización Pediatría 2018. Madrid: Lúa Ediciones 3.0; 2018. p. 507-526.",
        "- Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315(8):801–810. doi:10.1001/jama.2016.0287",
        "- Charles K, Lewis MJ, Montgomery E, Reid M. The 2021 Chronic Kidney Disease Epidemiology Collaboration Race-Free Estimated Glomerular Filtration Rate Equations in Kidney Disease: Leading the Way in Ending Disparities. Health Equity. 2024 Jan 12;8(1):39-45. doi: 10.1089/heq.2023.0038. PMID: 38250300; PMCID: PMC10797164.",
        "- Ohle R, O'Reilly F, O'Brien KK, Fahey T, Dimitrov BD. The Alvarado score for predicting acute appendicitis: a systematic review. BMC Med. 2011 Dec 28;9:139. doi: 10.1186/1741-7015-9-139. PMID: 22204638; PMCID: PMC3299622.",
        "- Interpretación del líquido cefalorraquídeo. (n.d.). Retrieved June 3, 2025, from https://www.elsevier.es/es-revista-anales-pediatria-continuada-51-pdf-S1696281814701647"
    ]

    #Informacion de referencias, terminos y condiciones, y privacidad
    info_panel = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.WHITE,
        elevation=8,
        divider_color=ft.Colors.WHITE,
        controls=[
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.MENU_BOOK, size=20),
                        ft.Text("Referencias bibliográficas", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[ft.Text(ref, size=14) for ref in referencias],
                        spacing=6
                    ),
                    padding=ft.padding.all(20)
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.GAVEL, size=20),
                        ft.Text("Términos de uso y condiciones", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Text(
                        "La información médica contenida en esta aplicación ha sido recopilada cuidadosamente con fines educativos y de apoyo clínico. "
                        "No obstante, el uso que se le dé a esta información es responsabilidad exclusiva del usuario. "
                        "MedCore no reemplaza el juicio clínico profesional ni la consulta médica especializada.\n\n"
                        "El usuario acepta que cualquier decisión tomada con base en los datos proporcionados por la app es de su entera responsabilidad.",
                        size=14,
                        text_align=ft.TextAlign.LEFT,
                    ),
                    padding=ft.padding.all(20),
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.LOCK, size=20),
                        ft.Text("Tratamiento de datos y privacidad", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Text(
                        "MedCore no recopila, transmite ni almacena información en servidores externos. "
                        "Toda la información ingresada, incluyendo historias clínicas, se guarda de manera local en el dispositivo del usuario.\n\n"
                        "Se recuerda que la historia clínica es un documento legal, privado y reservado. "
                        "Esta app fue diseñada únicamente como herramienta de organización de información médica para uso personal o profesional del usuario. "
                        "El manejo responsable y ético de los datos es esencial.",
                        size=14,
                        text_align=ft.TextAlign.LEFT,
                    ),
                    padding=ft.padding.all(20),
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
        ]
    )
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(height=20),
            ft.Container(content=creador_info),
            ft.Container(content=ft.Divider(thickness=1)),
            ft.Container(content=info_panel, padding=ft.padding.symmetric(horizontal=20)),
        ],
    )



