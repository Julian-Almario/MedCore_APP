import flet as ft
from modules.colors import *
from datetime import datetime, date, timedelta

def edad_gestacional_fur():
    fum_texto = ft.Text("FUM: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    edad_gestacional = ft.Text("Edad gestacional: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    fpp = ft.Text("Fecha probable de parto: -", text_align=ft.TextAlign.CENTER, color=ft.Colors.ON_SURFACE_VARIANT)

    date_picker_ref = ft.Ref[ft.DatePicker]()

    def calcular_edad_gestacional(fum_str):
        try:
            fum_date = datetime.strptime(fum_str, "%Y-%m-%d").date()
            hoy = date.today()
            dias = (hoy - fum_date).days

            if dias < 0:
                edad_gestacional.value = "Edad gestacional: FUM en el futuro"
                fpp.value = "Fecha probable de parto: -"
                fpp.color = ft.Colors.RED_400
            else:
                semanas = dias // 7
                dias_restantes = dias % 7
                edad_gestacional.value = f"Edad gestacional: {semanas} semanas y {dias_restantes} días"

                fpp_date = fum_date + timedelta(days=280)
                fpp.value = f"Fecha probable de parto: {fpp_date.strftime('%Y-%m-%d')}"

                if semanas <= 13:
                    fpp.color = ft.Colors.YELLOW_700
                elif 14 <= semanas <= 27:
                    fpp.color = ft.Colors.BLUE_400
                else:
                    fpp.color = ft.Colors.GREEN_400

        except Exception:
            edad_gestacional.value = "Edad gestacional: Fecha inválida"
            fpp.value = "Fecha probable de parto: -"
            fpp.color = ft.Colors.RED_400

        edad_gestacional.update()
        fpp.update()

    def on_fum_selected(e):
        if e.data:
            fum_date = datetime.fromisoformat(e.data).date()
            fum_str = fum_date.strftime("%Y-%m-%d")
            fum_texto.value = f"FUM: {fum_str}"
            fum_texto.update()
            calcular_edad_gestacional(fum_str)

    date_picker = ft.DatePicker(
        ref=date_picker_ref,
        on_change=on_fum_selected
    )

    def abrir_date_picker(e):
        e.page.dialog = date_picker_ref.current
        date_picker_ref.current.open = True
        e.page.update()

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            fum_texto.value = "FUM: -"
            edad_gestacional.value = "Edad gestacional: -"
            fpp.value = "Fecha probable de parto: -"
            fpp.color = ft.Colors.ON_SURFACE_VARIANT
            fum_texto.update()
            edad_gestacional.update()
            fpp.update()

    return ft.ExpansionPanelList(
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Edad gestacional por FUM", color=TEXT_COLOR),
                    subtitle=ft.Text("Cálculo a partir de la fecha de última menstruación", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Seleccionar FUM",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=abrir_date_picker,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.with_opacity(0.15, TEXT_COLOR),
                                    color=TEXT_COLOR,
                                    padding=ft.padding.symmetric(vertical=12, horizontal=20),
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                )
                            ),
                            fum_texto,
                            edad_gestacional,
                            fpp,
                            date_picker
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False
            )
        ]
    )


def edad_corregida_prematuro():
    fn_texto = ft.Text("Fecha de nacimiento: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    edad_cronologica = ft.Text("Edad cronológica: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    edad_corregida = ft.Text("Edad corregida: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    texto_ecuacion = ft.Text(
        "Fórmula: Edad corregida = Edad cronológica (semanas) - (40 - Edad gestacional al nacer)",
        text_align=ft.TextAlign.CENTER,
        size=12,
        color=TEXT_COLOR,
        italic=True
    )

    date_picker_ref = ft.Ref[ft.DatePicker]()
    eg_input = ft.TextField(label="Edad gestacional al nacer (semanas)", width=300, on_change=lambda e: on_eg_change(e))

    fecha_nacimiento_seleccionada = {"valor": None}

    def calcular_edades(fecha_nac_str, eg_nacimiento_str):
        try:
            fnac = datetime.strptime(fecha_nac_str, "%Y-%m-%d").date()
            hoy = date.today()
            edad_crono_dias = (hoy - fnac).days

            if edad_crono_dias < 0:
                edad_cronologica.value = "Edad cronológica: Fecha en el futuro"
                edad_cronologica.color = ft.Colors.RED
                edad_corregida.value = "Edad corregida: -"
                edad_corregida.color = TEXT_COLOR
                texto_ecuacion.value = ""
            else:
                semanas_crono = edad_crono_dias // 7
                dias_restantes = edad_crono_dias % 7

                # Desglose edad cronológica
                años_crono = semanas_crono // 52
                semanas_rest_crono = semanas_crono % 52
                meses_crono = semanas_rest_crono // 4
                semanas_finales_crono = semanas_rest_crono % 4

                partes_crono = []
                if años_crono > 0:
                    partes_crono.append(f"{años_crono} año{'s' if años_crono > 1 else ''}")
                if meses_crono > 0:
                    partes_crono.append(f"{meses_crono} mes{'es' if meses_crono > 1 else ''}")
                if semanas_finales_crono > 0:
                    partes_crono.append(f"{semanas_finales_crono} semana{'s' if semanas_finales_crono > 1 else ''}")
                if not partes_crono:
                    partes_crono.append("0 semanas")

                texto_edad_crono = ", ".join(partes_crono)
                edad_cronologica.value = f"Edad cronológica: {semanas_crono} semanas y {dias_restantes} días ({texto_edad_crono})"
                edad_cronologica.color = TEXT_COLOR

                eg_nacimiento = int(eg_nacimiento_str)
                semanas_prematuro = 40 - eg_nacimiento
                semanas_corr = semanas_crono - semanas_prematuro
                semanas_corr = max(semanas_corr, 0)

                # Desglose edad corregida
                años = semanas_corr // 52
                semanas_restantes = semanas_corr % 52
                meses = semanas_restantes // 4
                semanas_finales = semanas_restantes % 4

                partes = []
                if años > 0:
                    partes.append(f"{años} año{'s' if años > 1 else ''}")
                if meses > 0:
                    partes.append(f"{meses} mes{'es' if meses > 1 else ''}")
                if semanas_finales > 0:
                    partes.append(f"{semanas_finales} semana{'s' if semanas_finales > 1 else ''}")
                if not partes:
                    partes.append("0 semanas")

                texto_edad_corregida = ", ".join(partes)

                if semanas_corr < 12:
                    edad_corregida.color = ft.Colors.ORANGE
                elif 12 <= semanas_corr < 24:
                    edad_corregida.color = ft.Colors.BLUE
                else:
                    edad_corregida.color = ft.Colors.GREEN

                edad_corregida.value = f"Edad corregida: {semanas_corr} semanas ({texto_edad_corregida})"
                texto_ecuacion.value = f"Fórmula: {semanas_crono} - (40 - {eg_nacimiento}) = {semanas_corr} semanas"
        except Exception:
            edad_cronologica.value = "Edad cronológica: Error en datos"
            edad_cronologica.color = ft.Colors.RED
            edad_corregida.value = "Edad corregida: -"
            edad_corregida.color = TEXT_COLOR
            texto_ecuacion.value = ""

        edad_cronologica.update()
        edad_corregida.update()
        texto_ecuacion.update()

    def on_fnac_selected(e):
        if e.data:
            fnac_str = datetime.fromisoformat(e.data).strftime("%Y-%m-%d")
            fn_texto.value = f"Fecha de nacimiento: {fnac_str}"
            fn_texto.update()

            fecha_nacimiento_seleccionada["valor"] = fnac_str

            if eg_input.value.isdigit():
                calcular_edades(fnac_str, eg_input.value)

    def on_eg_change(e):
        if fecha_nacimiento_seleccionada["valor"] and eg_input.value.isdigit():
            calcular_edades(fecha_nacimiento_seleccionada["valor"], eg_input.value)

    date_picker = ft.DatePicker(
        ref=date_picker_ref,
        on_change=on_fnac_selected
    )

    def abrir_date_picker(e):
        e.page.dialog = date_picker_ref.current
        date_picker_ref.current.open = True
        e.page.update()

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

        if not is_expanded:
            fn_texto.value = "Fecha de nacimiento: -"
            edad_cronologica.value = "Edad cronológica: -"
            edad_corregida.value = "Edad corregida: -"
            texto_ecuacion.value = "Fórmula: Edad corregida = Edad cronológica (semanas) - (40 - Edad gestacional al nacer)"
            edad_cronologica.color = TEXT_COLOR
            edad_corregida.color = TEXT_COLOR
            eg_input.value = ""
            fecha_nacimiento_seleccionada["valor"] = None
            fn_texto.update()
            edad_cronologica.update()
            edad_corregida.update()
            texto_ecuacion.update()
            eg_input.update()

    return ft.ExpansionPanelList(
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Edad corregida del prematuro", color=TEXT_COLOR),
                    subtitle=ft.Text("Calculada a partir de la edad gestacional al nacer", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Seleccionar fecha de nacimiento",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=abrir_date_picker,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.with_opacity(0.15, TEXT_COLOR),
                                    color=TEXT_COLOR,
                                    padding=ft.padding.symmetric(vertical=12, horizontal=20),
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                )
                            ),
                            eg_input,
                            fn_texto,
                            edad_cronologica,
                            edad_corregida,
                            texto_ecuacion,
                            date_picker
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False
            )
        ]
    )

def bishop():
    opciones_bishop = {
        "Dilatación (cm)": ["Cerrado", "1–2", "3–4", "≥5"],
        "Borramiento (%)": ["0–30", "40–50", "60–70", "≥80"],
        "Estación fetal": ["–3", "–2", "–1/0", "+1/+2"],
        "Consistencia cervical": ["Firme", "Media", "Blanda"],
        "Posición cervical": ["Posterior", "Media", "Anterior"],
    }

    # Mapeo de puntajes según índice en la lista
    selectores = {}
    for criterio, opciones in opciones_bishop.items():
        selectores[criterio] = ft.Dropdown(
            options=[ft.dropdown.Option(opcion) for opcion in opciones],
            label=criterio,
            width=400,
        )

    resultado_bishop = ft.Text("Puntaje total: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    interpretacion_bishop = ft.Text("Interpretación: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)

    def calcular_bishop(e):
        puntaje = 0
        incompleto = False

        for criterio, dropdown in selectores.items():
            if dropdown.value is None:
                incompleto = True
                continue
            opciones = opciones_bishop[criterio]
            indice = opciones.index(dropdown.value)
            puntaje += indice

        if incompleto:
            resultado_bishop.value = "Puntaje total: -"
            interpretacion_bishop.value = "Interpretación: Selecciona todos los parámetros."
            resultado_bishop.color = TEXT_COLOR
            interpretacion_bishop.color = TEXT_COLOR
        else:
            if puntaje >= 7:
                interpretacion = "Inducción trabajo de parto"
                color = "green"
            elif puntaje <= 6:
                interpretacion = "Maduración cervical"
                color = "orange"
            else:
                interpretacion = "Condiciones desfavorables para inducción."
                color = "red"
            resultado_bishop.value = f"Puntaje total: {puntaje}"
            interpretacion_bishop.value = f"Interpretación: {interpretacion}"
            resultado_bishop.color = color
            interpretacion_bishop.color = color

        resultado_bishop.update()
        interpretacion_bishop.update()

    for dropdown in selectores.values():
        dropdown.on_change = calcular_bishop

    panel_ref = ft.Ref[ft.ExpansionPanel]()
    panel_list_ref = ft.Ref[ft.ExpansionPanelList]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()
        if not is_expanded:
            for d in selectores.values():
                d.value = None
                d.update()
            resultado_bishop.value = "Puntaje total: -"
            interpretacion_bishop.value = "Interpretación: -"
            resultado_bishop.update()
            interpretacion_bishop.update()

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
                    title=ft.Text("Índice de Bishop para inducción del parto", color=TEXT_COLOR),
                    subtitle=ft.Text("Evaluación obstétrica", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=list(selectores.values()) + [resultado_bishop, interpretacion_bishop],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False,
            )
        ],
    )

def semanas_gestacion_por_ecografia():
    fecha_eco_texto = ft.Text("Fecha de la primera ecografía: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    eg_actual_texto = ft.Text("Edad gestacional actual: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    fecha_probable_parto = ft.Text("Fecha probable de parto: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    texto_ecuacion = ft.Text(
        "Fórmula: EG actual = Semanas + días desde FUR estimada",
        text_align=ft.TextAlign.CENTER,
        size=12,
        color=TEXT_COLOR,
        italic=True
    )

    date_picker_ref = ft.Ref[ft.DatePicker]()

    eg_semanas_input = ft.TextField(label="Semanas (EG ecografía)", width=200, on_change=lambda e: on_eg_change(e))
    eg_dias_input = ft.TextField(label="Días (0-6)", width=100, on_change=lambda e: on_eg_change(e))

    fecha_ecografia_seleccionada = {"valor": None}

    def calcular_eg(fecha_eco_str, semanas_str, dias_str):
        try:
            fecha_eco = datetime.strptime(fecha_eco_str, "%Y-%m-%d").date()
            hoy = date.today()

            semanas = int(semanas_str) if semanas_str.isdigit() else 0
            dias = int(dias_str) if dias_str.isdigit() else 0
            if dias < 0 or dias > 6:
                raise ValueError("Los días deben estar entre 0 y 6")

            # Calcular FUR estimada
            fur_estimada = fecha_eco - timedelta(weeks=semanas, days=dias)

            # EG actual en semanas y días
            dias_gestacion = (hoy - fur_estimada).days
            semanas_gestacion = dias_gestacion // 7
            dias_restantes = dias_gestacion % 7

            eg_actual_texto.value = f"Edad gestacional actual: {semanas_gestacion} semanas + {dias_restantes} días"
            eg_actual_texto.color = TEXT_COLOR

            # Calcular fecha probable de parto
            fpp = fur_estimada + timedelta(weeks=40)
            fecha_probable_parto.value = f"Fecha probable de parto: {fpp.strftime('%Y-%m-%d')}"

            texto_ecuacion.value = f"Fórmula: EG actual = {dias_gestacion} días desde FUR ({fur_estimada})"

        except Exception:
            eg_actual_texto.value = "Edad gestacional actual: Error en datos"
            eg_actual_texto.color = ft.Colors.RED
            fecha_probable_parto.value = "Fecha probable de parto: -"
            texto_ecuacion.value = ""

        eg_actual_texto.update()
        fecha_probable_parto.update()
        texto_ecuacion.update()

    def on_fecha_eco_selected(e):
        if e.data:
            fecha_eco_str = datetime.fromisoformat(e.data).strftime("%Y-%m-%d")
            fecha_eco_texto.value = f"Fecha de la primera ecografía: {fecha_eco_str}"
            fecha_eco_texto.update()

            fecha_ecografia_seleccionada["valor"] = fecha_eco_str

            if eg_semanas_input.value.isdigit() and eg_dias_input.value.isdigit():
                calcular_eg(fecha_eco_str, eg_semanas_input.value, eg_dias_input.value)

    def on_eg_change(e):
        if fecha_ecografia_seleccionada["valor"]:
            if eg_semanas_input.value.isdigit() and eg_dias_input.value.isdigit():
                calcular_eg(fecha_ecografia_seleccionada["valor"], eg_semanas_input.value, eg_dias_input.value)

    date_picker = ft.DatePicker(
        ref=date_picker_ref,
        on_change=on_fecha_eco_selected
    )

    def abrir_date_picker(e):
        e.page.dialog = date_picker_ref.current
        date_picker_ref.current.open = True
        e.page.update()

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

        if not is_expanded:
            fecha_eco_texto.value = "Fecha de la primera ecografía: -"
            eg_actual_texto.value = "Edad gestacional actual: -"
            fecha_probable_parto.value = "Fecha probable de parto: -"
            texto_ecuacion.value = "Fórmula: EG actual = Semanas + días desde FUR estimada"
            eg_actual_texto.color = TEXT_COLOR
            eg_semanas_input.value = ""
            eg_dias_input.value = ""
            fecha_ecografia_seleccionada["valor"] = None
            fecha_eco_texto.update()
            eg_actual_texto.update()
            fecha_probable_parto.update()
            texto_ecuacion.update()
            eg_semanas_input.update()
            eg_dias_input.update()

    return ft.ExpansionPanelList(
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Edad gestacional por primera ecografía", color=TEXT_COLOR),
                    subtitle=ft.Text("Calculada con semanas + días estimados en la ecografía", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Seleccionar fecha de la ecografía",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=abrir_date_picker,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.with_opacity(0.15, TEXT_COLOR),
                                    color=TEXT_COLOR,
                                    padding=ft.padding.symmetric(vertical=12, horizontal=20),
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                )
                            ),
                            ft.Row([eg_semanas_input, eg_dias_input], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                            fecha_eco_texto,
                            eg_actual_texto,
                            fecha_probable_parto,
                            texto_ecuacion,
                            date_picker
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False
            )
        ]
    )

def semanas_gestacion_por_fpp():
    fecha_fpp_texto = ft.Text("Fecha probable de parto: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    eg_actual_texto = ft.Text("Edad gestacional actual: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    fur_estimada_texto = ft.Text("FUR estimada: -", text_align=ft.TextAlign.CENTER, color=TEXT_COLOR)
    texto_ecuacion = ft.Text(
        "Fórmula: EG actual = Semanas + días desde FUR estimada",
        text_align=ft.TextAlign.CENTER,
        size=12,
        color=TEXT_COLOR,
        italic=True
    )

    date_picker_ref = ft.Ref[ft.DatePicker]()
    fecha_fpp_seleccionada = {"valor": None}

    def calcular_eg(fecha_fpp_str):
        try:
            fecha_fpp = datetime.strptime(fecha_fpp_str, "%Y-%m-%d").date()
            hoy = date.today()

            # Calcular FUR estimada
            fur_estimada = fecha_fpp - timedelta(weeks=40)

            # Calcular EG actual
            dias_gestacion = (hoy - fur_estimada).days
            semanas_gestacion = dias_gestacion // 7
            dias_restantes = dias_gestacion % 7

            fur_estimada_texto.value = f"FUR estimada: {fur_estimada.strftime('%Y-%m-%d')}"
            eg_actual_texto.value = f"Edad gestacional actual: {semanas_gestacion} semanas + {dias_restantes} días"
            eg_actual_texto.color = TEXT_COLOR

            texto_ecuacion.value = f"Fórmula: EG actual = {dias_gestacion} días desde FUR ({fur_estimada})"

        except Exception:
            eg_actual_texto.value = "Edad gestacional actual: Error en datos"
            eg_actual_texto.color = ft.Colors.RED
            fur_estimada_texto.value = "FUR estimada: -"
            texto_ecuacion.value = ""

        fur_estimada_texto.update()
        eg_actual_texto.update()
        texto_ecuacion.update()

    def on_fecha_fpp_selected(e):
        if e.data:
            fecha_fpp_str = datetime.fromisoformat(e.data).strftime("%Y-%m-%d")
            fecha_fpp_texto.value = f"Fecha probable de parto: {fecha_fpp_str}"
            fecha_fpp_texto.update()

            fecha_fpp_seleccionada["valor"] = fecha_fpp_str
            calcular_eg(fecha_fpp_str)

    date_picker = ft.DatePicker(
        ref=date_picker_ref,
        on_change=on_fecha_fpp_selected
    )

    def abrir_date_picker(e):
        e.page.dialog = date_picker_ref.current
        date_picker_ref.current.open = True
        e.page.update()

    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        is_expanded = panel.expanded
        panel.bgcolor = SECONDARY_COLOR if is_expanded else PRIMARY_COLOR
        panel.update()

        if not is_expanded:
            fecha_fpp_texto.value = "Fecha probable de parto: -"
            eg_actual_texto.value = "Edad gestacional actual: -"
            fur_estimada_texto.value = "FUR estimada: -"
            texto_ecuacion.value = "Fórmula: EG actual = Semanas + días desde FUR estimada"
            eg_actual_texto.color = TEXT_COLOR
            fecha_fpp_seleccionada["valor"] = None
            fecha_fpp_texto.update()
            eg_actual_texto.update()
            fur_estimada_texto.update()
            texto_ecuacion.update()

    return ft.ExpansionPanelList(
        on_change=on_expand_change,
        expand_icon_color=TEXT_COLOR,
        elevation=8,
        divider_color=TEXT_COLOR,
        controls=[
            ft.ExpansionPanel(
                ref=panel_ref,
                header=ft.ListTile(
                    title=ft.Text("Edad gestacional por FPP", color=TEXT_COLOR),
                    subtitle=ft.Text("Calculada a partir de la fecha probable de parto", size=SUBTITLE_SIZE, color=TEXT_COLOR)
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Seleccionar fecha probable de parto",
                                icon=ft.Icons.CALENDAR_MONTH,
                                on_click=abrir_date_picker,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.with_opacity(0.15, TEXT_COLOR),
                                    color=TEXT_COLOR,
                                    padding=ft.padding.symmetric(vertical=12, horizontal=20),
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                )
                            ),
                            fecha_fpp_texto,
                            fur_estimada_texto,
                            eg_actual_texto,
                            texto_ecuacion,
                            date_picker
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(vertical=25, horizontal=50),
                    alignment=ft.alignment.center
                ),
                bgcolor=PRIMARY_COLOR,
                expanded=False
            )
        ]
    )
