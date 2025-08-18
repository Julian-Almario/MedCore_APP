import os
import json
import flet as ft
from datetime import date, datetime, timedelta

# Ruta de almacenamiento
RUTA_HISTORIAS = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "storage", "data", "historias")
)
os.makedirs(RUTA_HISTORIAS, exist_ok=True)
ARCHIVO_HISTORIAS = os.path.join(RUTA_HISTORIAS, "historias.json")

# Crear archivo vacío si no existe
if not os.path.exists(ARCHIVO_HISTORIAS):
    with open(ARCHIVO_HISTORIAS, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

def cargar_historias():
    try:
        with open(ARCHIVO_HISTORIAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_todas_las_historias(historias):
    with open(ARCHIVO_HISTORIAS, "w", encoding="utf-8") as f:
        json.dump(historias, f, ensure_ascii=False, indent=4)

def guardar_historia_en_json(historia: dict):
    historias = cargar_historias()
    historias.append(historia)
    guardar_todas_las_historias(historias)

def _panel_de_historia(hist: dict, index: int, refrescar_lista, page) -> ft.ExpansionPanel:
    panel_ref = ft.Ref[ft.ExpansionPanel]()

    def on_expand_change(e):
        panel = panel_ref.current
        if panel:
            panel.bgcolor = "#2E2E2E" if panel.expanded else "#1E1E1E"
            panel.update()

    # Acción borrar
    def borrar_historia_click(e):
        historias = cargar_historias()
        del historias[index]
        guardar_todas_las_historias(historias)
        refrescar_lista()
        page.snack_bar = ft.SnackBar(ft.Text("Historia eliminada"), open=True)
        page.update()

    # Acción editar
    def editar_historia_click(e):
        mostrar_formulario_historia(page, refrescar_lista, historia_existente=hist, index=index)

    contenido_panel = [
        ft.Text(f"Fecha: {hist.get('fecha', 'N/A')}"),
        ft.Text(f"Nombre del paciente: {hist.get('nombre', '')}"),
        ft.Text(f"Iedntificación: {hist.get('identificacion', '')}"),
        ft.Text(f"Estado civil: {hist.get('estado civil', '')}"),
        ft.Text(f"Edad: {hist.get('edad', '')}"),
        ft.Text(f"Fecha de nacimiento: {hist.get('fecha_nacimiento', '')}"),
        ft.Text(f"Sexo: {hist.get('sexo', '')}"),
        ft.Text(f"Hemoclasificación: {hist.get('hemoclasificacion', '')}"),
        ft.Text(f"Escolaridad: {hist.get('escolaridad', '')}"),
        ft.Text(f"Ocupación: {hist.get('ocupacion', '')}"),
        ft.Text(f"Dirección de residencia: {hist.get('direccion', '')}"),
        ft.Text(f"Parentesco con acompañante: {hist.get('acomp_parentesco', '')}"),
        ft.Text(f"Nombre de acompañante: {hist.get('acomp_nombre', '')}"),
        ft.Text(f"EPS: {hist.get('eps', '')}"),
        ft.Text(f"Fuente información: {hist.get('fuente_info', '')}"),
        ft.Text(f"Confianza de información: {hist.get('confianza_info', '')}"),
        ft.Text(f"Motivo de consulta: {hist.get('motivo', '')}"),
        ft.Text(f"Enfermedad actual: {hist.get('enfermedad actual', '')}"),
        ft.Divider(),
        ft.Text(f"Revision por sistemas: {hist.get('rev_sis', '')}"),
        ft.Row([
            ft.ElevatedButton("Editar", on_click=editar_historia_click),
            ft.ElevatedButton("Borrar", on_click=borrar_historia_click, bgcolor="red", color="white")
        ])
    ]

    extra = hist.get("extra", {})
    if extra:
        for clave, valor in extra.items():
            contenido_panel.insert(-1, ft.Text(f"{clave}: {valor}"))

    return ft.ExpansionPanel(
        ref=panel_ref,
        header=ft.ListTile(
            title=ft.Text(hist.get("nombre", "Sin nombre")),
            subtitle=ft.Text(f"{hist.get('formato', 'N/A')} · {hist.get('identificacion', '')}"),
        ),
        content=ft.Container(content=ft.Column(controls=contenido_panel), padding=15),
        bgcolor="#1E1E1E",
        expanded=False,
    )

def mostrar_formulario_historia(page, refrescar_lista, historia_existente=None, index=None):
    historia_existente = historia_existente or {}

    # Campo de solo lectura para mostrar fecha
    fecha_nacimiento_input = ft.TextField(
        label="Fecha de nacimiento",
        value=historia_existente.get("fecha_nacimiento", ""),
        read_only=True,
        width=True
    )

    # Ref del DatePicker
    date_picker_ref = ft.Ref[ft.DatePicker]()



    # Cuando se selecciona la fecha
    def on_fecha_selected(e):
        if e.data:
            fecha_sel = datetime.fromisoformat(e.data).date()
            fecha_str = fecha_sel.strftime("%Y-%m-%d")
            fecha_nacimiento_input.value = fecha_str
            # Calcular edad
            hoy = date.today()
            edad = hoy.year - fecha_sel.year - ((hoy.month, hoy.day) < (fecha_sel.month, fecha_sel.day))
            edad_input.value = str(edad)
            fecha_nacimiento_input.update()
            edad_input.update()


    # DatePicker
    date_picker = ft.DatePicker(
        ref=date_picker_ref,
        on_change=on_fecha_selected
    )

    # Botón para abrir el DatePicker
    def abrir_date_picker(e):
        e.page.dialog = date_picker_ref.current
        date_picker_ref.current.open = True
        e.page.update()

    boton_fecha = ft.ElevatedButton(
        "Fecha de nacimiento",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_date_picker
    )

    page.overlay.append(date_picker)  # Necesario para que funcione el selector

    formato_dropdown = ft.Dropdown(
        label="Formato de historia clínica",
        options=[
            ft.dropdown.Option("Medicina General"),
            ft.dropdown.Option("Pediatría"),
            ft.dropdown.Option("Ginecología"),
        ],
        width=450,
        value=historia_existente.get("formato")
    )
    # Campo de solo lectura para mostrar la fecha de la historia
    fecha_input = ft.TextField(
        label="Fecha de la historia",
        value=historia_existente.get("fecha", ""),
        read_only=True,
        width=True
    )

    # Ref del DatePicker
    fecha_historia_ref = ft.Ref[ft.DatePicker]()

    # Cuando se selecciona la fecha
    fecha_historia_change_callbacks = []

    def on_fecha_historia_selected(e):
        if e.data:
            fecha_sel = datetime.fromisoformat(e.data).date()
            fecha_str = fecha_sel.strftime("%Y-%m-%d")
            fecha_input.value = fecha_str
            fecha_input.update()
            
            for cb in fecha_historia_change_callbacks:
                try:
                    cb()
                except Exception:
                    pass
            page.update()

    # DatePicker
    date_picker_historia = ft.DatePicker(
        ref=fecha_historia_ref,
        on_change=on_fecha_historia_selected
    )

    # Botón para abrir el DatePicker
    def abrir_date_picker_historia(e):
        e.page.dialog = fecha_historia_ref.current
        fecha_historia_ref.current.open = True
        e.page.update()

    boton_fecha_historia = ft.ElevatedButton(
        "Seleccionar fecha historia",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_date_picker_historia
    )

    page.overlay.append(date_picker_historia)



    # Campos de identificacion
    estado_civil_dropdown = ft.Dropdown(
        label="Estado civil",
        options=[ft.dropdown.Option(o) for o in ["Soltero", "Casado", "Divorciado", "Viudo", "Unión libre"]],
        width=450,
        value=historia_existente.get("estado civil", "")
    )

    edad_input = ft.TextField(label="Edad", read_only=True, value="", width=True)

    sexo_dropdown = ft.Dropdown(
        label="Sexo",
        options=[ft.dropdown.Option(o) for o in ["Masculino", "Femenino", "Otro"]],
        width=450,
        value=historia_existente.get("sexo", "")
    )

    hemoclasificacion_dropdown = ft.Dropdown(
        label="Hemoclasificación",
        options=[ft.dropdown.Option(o) for o in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]],
        width=450,
        value=historia_existente.get("hemoclasificacion", "")
    )

    escolaridad_dropdown = ft.Dropdown(
        label="Escolaridad",
        options=[ft.dropdown.Option(o) for o in ["Primaria", "Secundaria", "Bachiller", "Tecnico", "Universitario"]],
        width=450,
        value=historia_existente.get("escolaridad", "")
    )
    direccion_input = ft.TextField(label="Dirección y Lugar de residencia",width=True, value=historia_existente.get("direccion", ""))
    acomp_nombre_input = ft.TextField(label="Nombre Acompañante",width=True, value=historia_existente.get("acomp_nombre", ""))
    acomp_parentesco_dropdown = ft.Dropdown(
        label="Parentesco del acompañante",
        options=[ft.dropdown.Option(o) for o in ["Sin acompañante","Madre", "Padre", "Herman@", "Ti@", "Amig@", "Pareja", "Espos@"]],
        width=450,
        value=historia_existente.get("acomp_parentesco", "")
    )
    ocupacion_input = ft.TextField(label="Ocupación", width=True, value=historia_existente.get("ocupacion", ""))

    eps_dropdown = ft.Dropdown(
        label="EPS",
        options=[ft.dropdown.Option(o) for o in ["Nueva EPS", "Savia", "FOMAG", "Sura", "Sanitas"]],
        width=450,
        value=historia_existente.get("eps", "")
    )

    fuente_info_dropdown = ft.Dropdown(
        label="Fuente de información",
        options=[ft.dropdown.Option(o) for o in ["Paciente", "Acompañante"]],
        width=450,
        value=historia_existente.get("fuente_info", "")
    )

    confianza_info_dropdown = ft.Dropdown(
        label="Confiabilidad de información",
        options=[ft.dropdown.Option(o) for o in ["Buena", "Moderada", "Mala"]],
        width=450,
        value=historia_existente.get("confianza_info", "")
    )

    nombre_input = ft.TextField(label="Nombre del paciente", value=historia_existente.get("nombre", ""))
    id_input = ft.TextField(label="Identificación", value=historia_existente.get("identificacion", ""))
    motivo_input = ft.TextField(label="Motivo de consulta", multiline=True, value=historia_existente.get("motivo", ""))
    enfermedadactual_input = ft.TextField(label="Enfermedad actual", multiline=True, width=True, value=historia_existente.get("enfermedad actual", ""))


    # Revision por sistemas
    rev_sis_input = ft.TextField(label="Revision por sistemas", multiline=True, value=historia_existente.get("rev_sis", ""))

    campos_extra = ft.Column()
    extra_data = historia_existente.get("extra", {})

    # Función para actualizar campos extra según formato
    def actualizar_campos_extra(ev):
        valores_actuales = {campo.label: campo.value for campo in campos_extra.controls if isinstance(campo, ft.TextField)}
        campos_extra.controls.clear()

        def valor_guardado(clave):
            return valores_actuales.get(clave, extra_data.get(clave, ""))

        if formato_dropdown.value == "Ginecología":
            # --- Calculadora de Edad Gestacional por ecografía ---
            fecha_eco_input = ft.TextField(
                label="Fecha primera ecografía",
                value=valor_guardado("Fecha primera ecografía"),
                read_only=True,
                width=450
            )

            eg_semanas_input = ft.TextField(label="Semanas (EG ecografía)", width=450, value=valor_guardado("EG Semanas"))
            eg_dias_input = ft.TextField(label="Días (0-6)", width=450, value=valor_guardado("EG Días"))
            fur_output = ft.TextField(label="Fecha última menstruación (estimada)", width=450, read_only=True, value=valor_guardado("FUR estimada"))
            eg_actual_output = ft.TextField(label="Edad gestacional actual", width=450, read_only=True, value=valor_guardado("Edad gestacional actual"))
            fpp_output = ft.TextField(label="Fecha probable de parto", width=450, read_only=True, value=valor_guardado("Fecha probable de parto"))

            # Ref para el DatePicker de ecografía
            date_picker_eco_ref = ft.Ref[ft.DatePicker]()

            
            def calcular_eg(e=None):
                try:
                    if not fecha_eco_input.value or not fecha_input.value:
                        return


                    fecha_eco = datetime.strptime(fecha_eco_input.value, "%Y-%m-%d").date()
                    hoy = datetime.strptime(fecha_input.value, "%Y-%m-%d").date()

                    semanas = int(eg_semanas_input.value.strip()) if eg_semanas_input.value.strip().isdigit() else 0
                    dias = int(eg_dias_input.value.strip()) if eg_dias_input.value.strip().isdigit() else 0
                    if dias < 0 or dias > 6:
                        dias = 0

                    # estimamos FUR a partir de la eco
                    fur_estimada = fecha_eco - timedelta(weeks=semanas, days=dias)
                    fur_output.value = fur_estimada.strftime("%Y-%m-%d")

                    # edad gestacional en dias desde FUR hasta 'hoy' (fecha de la historia)
                    dias_gestacion = (hoy - fur_estimada).days
                    if dias_gestacion < 0:
                        # fecha de historia anterior a la FUR estimada → no tiene sentido
                        eg_actual_output.value = "EG: datos inconsistentes"
                        fpp_output.value = "-"
                    else:
                        semanas_gestacion = dias_gestacion // 7
                        dias_restantes = dias_gestacion % 7
                        eg_actual_output.value = f"{semanas_gestacion} semanas + {dias_restantes} días"
                        fpp_output.value = (fur_estimada + timedelta(weeks=40)).strftime("%Y-%m-%d")

                except Exception as ex:
                    eg_actual_output.value = "Error en datos"
                    fpp_output.value = "-"
                    fur_output.value = "-"

                # Refrescar controles y página
                fur_output.update()
                eg_actual_output.update()
                fpp_output.update()
                page.update()

            # Cuando selecciono fecha en el DatePicker de la ecografía
            def on_fecha_eco_selected(e):
                if e.data:
                    fecha_sel = datetime.fromisoformat(e.data).date()
                    fecha_eco_input.value = fecha_sel.strftime("%Y-%m-%d")
                    fecha_eco_input.update()
                    calcular_eg()

            # DatePicker de ecografía y botón para abrirlo usando pick_date()
            date_picker_eco = ft.DatePicker(ref=date_picker_eco_ref, on_change=on_fecha_eco_selected)

            def abrir_date_picker_eco(e):
                try:
                    date_picker_eco_ref.current.pick_date()
                except Exception:
                    e.page.dialog = date_picker_eco_ref.current
                    date_picker_eco_ref.current.open = True
                    e.page.update()

            boton_fecha_eco = ft.ElevatedButton(
                "Seleccionar fecha de la ecografía",
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=abrir_date_picker_eco
            )

            # Recalcular cuando cambian semanas/días manualmente
            eg_semanas_input.on_change = calcular_eg
            eg_dias_input.on_change = calcular_eg

            peso_input = ft.TextField(label="Peso (kg)", width=450, value=valor_guardado("Peso"))
            talla_input = ft.TextField(label="Talla (m)", width=450, value=valor_guardado("Talla"))
            imc_input = ft.TextField(label="IMC", width=450, read_only=True, value=valor_guardado("IMC"))

            def calcular_imc(e=None):
                try:
                    peso = float(peso_input.value)
                    talla = float(talla_input.value)
                    if talla > 0:
                        imc = peso / (talla ** 2)
                        imc_input.value = f"{imc:.2f}"
                except:
                    imc_input.value = ""
                imc_input.update()

            peso_input.on_change = calcular_imc
            talla_input.on_change = calcular_imc

            campos_extra.controls.extend([
                ft.Text("Antecedentes", size=16, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Antecedentes Patologico", multiline=True, width=450, value=valor_guardado("Antecedentes Patologico")),
                ft.TextField(label="Antecedentes Medicamentos", multiline=True, width=450, value=valor_guardado("Antecedentes Medicamentos")),
                ft.Text("Antecedentes ginecológicos", size=16, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Gestas", width=450, value=valor_guardado("Gestas")),
                ft.TextField(label="Partos", width=450, value=valor_guardado("Partos")),
                ft.TextField(label="Abortos", width=450, value=valor_guardado("Abortos")),
                ft.TextField(label="Cesáreas", width=450, value=valor_guardado("Cesáreas")),
                ft.Divider(),
                ft.Text("Cálculo Edad Gestacional por Ecografía", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([boton_fecha_eco], alignment=ft.MainAxisAlignment.CENTER),
                fecha_eco_input,
                eg_semanas_input,
                eg_dias_input,
                fur_output,
                eg_actual_output,
                fpp_output,
                ft.Divider(),
                date_picker_eco,
                ft.Divider(),
                ft.TextField(label="Antecedentes Hospitalizaciones", multiline=True, width=450, value=valor_guardado("Antecedentes Hospitalizaciones")),
                ft.TextField(label="Antecedentes Cirugias", multiline=True, width=450, value=valor_guardado("Antecedentes Cirugias")),
                ft.TextField(label="Antecedentes Traumaticos", multiline=True, width=450, value=valor_guardado("Antecedentes Traumaticos")),
                ft.TextField(label="Antecedentes Transfusiones", multiline=True, width=450, value=valor_guardado("Antecedentes Transfusiones")),
                ft.TextField(label="Antecedentes Alergicos", multiline=True, width=450, value=valor_guardado("Antecedentes Alergicos")),
                ft.TextField(label="Antecedentes Toxicologicos", multiline=True, width=450, value=valor_guardado("Antecedentes Toxicologicos")),
                ft.TextField(label="Antecedentes Familiares", multiline=True, width=450, value=valor_guardado("Antecedentes Familiares")),
                ft.TextField(label="Antecedentes Socioeconomicos", multiline=True, width=450, value=valor_guardado("Antecedentes Socioeconomicos")),
                ft.Divider(),
                ft.Text("Signos Vitales", size=16, weight=ft.FontWeight.BOLD),
                peso_input,
                talla_input,
                imc_input,
                ft.TextField(label="Frecuencia cardíaca (lpm)", width=450, value=valor_guardado("Frecuencia cardíaca")),
                ft.TextField(label="Frecuencia respiratoria (rpm)", width=450, value=valor_guardado("Frecuencia respiratoria")),
                ft.TextField(label="Tensión arterial (mmHg)", width=450, value=valor_guardado("Tensión arterial")),
                ft.TextField(label="Temperatura (°C)", width=450, value=valor_guardado("Temperatura")),
                ft.TextField(label="Examen Fisico", multiline=True, width=450, value=valor_guardado("Examen Fisico")),
                ft.Divider(),
                ft.TextField(label="Analisis", width=450, value=valor_guardado("Analisis")),
                ft.TextField(label="Impresion DX", width=450, value=valor_guardado("Impresion DX")),
                ft.TextField(label="Tratamiento", width=450, value=valor_guardado("Tratamiento")),
            ])


        elif formato_dropdown.value == "Pediatría":
            peso_input = ft.TextField(label="Peso (kg)", width=450, value=valor_guardado("Peso"))
            talla_input = ft.TextField(label="Talla (m)", width=450, value=valor_guardado("Talla"))
            imc_input = ft.TextField(label="IMC", width=450, read_only=True, value=valor_guardado("IMC"))

            # Función para calcular IMC automáticamente
            def calcular_imc(e=None):
                try:
                    peso = float(peso_input.value)
                    talla = float(talla_input.value)
                    if talla > 0:
                        imc = peso / (talla ** 2)
                        imc_input.value = f"{imc:.2f}"
                        imc_input.update()
                except:
                    imc_input.value = ""
                    imc_input.update()

            # Eventos para recalcular IMC
            peso_input.on_change = calcular_imc
            talla_input.on_change = calcular_imc
            campos_extra.controls.extend([
                ft.Text("Antecedentes", size=16, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Antecedentes Patologico", multiline=True, width=450, value=valor_guardado("Antecedentes Patologico")),
                ft.TextField(label="Antecedentes Medicamentos", multiline=True, width=450, value=valor_guardado("Antecedentes Medicamentos")),
                ft.TextField(label="Antecedentes Hospitalizaciones", multiline=True, width=450, value=valor_guardado("Antecedentes Hospitalizaciones")),
                ft.TextField(label="Antecedentes Cirugias", multiline=True, width=450, value=valor_guardado("Antecedentes Cirugias")),
                ft.TextField(label="Antecedentes Traumaticos", multiline=True, width=450, value=valor_guardado("Antecedentes Traumaticos")),
                ft.TextField(label="Antecedentes Transfusiones", multiline=True, width=450, value=valor_guardado("Antecedentes Transfusiones")),
                ft.TextField(label="Antecedentes Alergicos", multiline=True, width=450, value=valor_guardado("Antecedentes Alergicos")),
                ft.TextField(label="Antecedentes Toxicologicos", multiline=True, width=450, value=valor_guardado("Antecedentes Toxicologicos")),
                ft.TextField(label="Antecedentes Familiares", multiline=True, width=450, value=valor_guardado("Antecedentes Familiares")),
                ft.TextField(label="Antecedentes Socioeconomicos", multiline=True, width=450, value=valor_guardado("Antecedentes Socioeconomicos")),
                ft.TextField(label="Edad gestacional al nacer", width=450, value=valor_guardado("Edad gestacional al nacer")),
                ft.Text("Signos Vitales", size=16, weight=ft.FontWeight.BOLD),
                peso_input,
                talla_input,
                imc_input,
                ft.TextField(label="Frecuencia cardíaca (lpm)", width=450, value=valor_guardado("Frecuencia cardíaca")),
                ft.TextField(label="Frecuencia respiratoria (rpm)", width=450, value=valor_guardado("Frecuencia respiratoria")),
                ft.TextField(label="Tensión arterial (mmHg)", width=450, value=valor_guardado("Tensión arterial")),
                ft.TextField(label="Temperatura (°C)", width=450, value=valor_guardado("Temperatura")),
                ft.TextField(label="Examen Fisico", multiline=True, width=450, value=valor_guardado("Examen Fisico")),
                ft.Divider(),
                ft.TextField(label="Analisis", width=450, value=valor_guardado("Analisis")),
                ft.TextField(label="Impresion DX", width=450, value=valor_guardado("Impresion DX")),
                ft.TextField(label="Tratamiento", width=450, value=valor_guardado("Tratamiento")),
            ])
        elif formato_dropdown.value == "Medicina General":
            peso_input = ft.TextField(label="Peso (kg)", width=450, value=valor_guardado("Peso"))
            talla_input = ft.TextField(label="Talla (m)", width=450, value=valor_guardado("Talla"))
            imc_input = ft.TextField(label="IMC", width=450, read_only=True, value=valor_guardado("IMC"))

            # Función para calcular IMC automáticamente
            def calcular_imc(e=None):
                try:
                    peso = float(peso_input.value)
                    talla = float(talla_input.value)
                    if talla > 0:
                        imc = peso / (talla ** 2)
                        imc_input.value = f"{imc:.2f}"
                        imc_input.update()
                except:
                    imc_input.value = ""
                    imc_input.update()

            # Eventos para recalcular IMC
            peso_input.on_change = calcular_imc
            talla_input.on_change = calcular_imc

            campos_extra.controls.extend([
                ft.Text("Antecedentes", size=16, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Antecedentes Patologico", multiline=True, width=450, value=valor_guardado("Antecedentes Patologico")),
                ft.TextField(label="Antecedentes Medicamentos", multiline=True, width=450, value=valor_guardado("Antecedentes Medicamentos")),
                ft.TextField(label="Antecedentes Hospitalizaciones", multiline=True, width=450, value=valor_guardado("Antecedentes Hospitalizaciones")),
                ft.TextField(label="Antecedentes Cirugias", multiline=True, width=450, value=valor_guardado("Antecedentes Cirugias")),
                ft.TextField(label="Antecedentes Traumaticos", multiline=True, width=450, value=valor_guardado("Antecedentes Traumaticos")),
                ft.TextField(label="Antecedentes Transfusiones", multiline=True, width=450, value=valor_guardado("Antecedentes Transfusiones")),
                ft.TextField(label="Antecedentes Alergicos", multiline=True, width=450, value=valor_guardado("Antecedentes Alergicos")),
                ft.TextField(label="Antecedentes Toxicologicos", multiline=True, width=450, value=valor_guardado("Antecedentes Toxicologicos")),
                ft.TextField(label="Antecedentes Familiares", multiline=True, width=450, value=valor_guardado("Antecedentes Familiares")),
                ft.TextField(label="Antecedentes Socioeconomicos", multiline=True, width=450, value=valor_guardado("Antecedentes Socioeconomicos")),
                ft.Divider(),
                ft.Text("Signos Vitales", size=16, weight=ft.FontWeight.BOLD),
                peso_input,
                talla_input,
                imc_input,
                ft.TextField(label="Frecuencia cardíaca (lpm)", width=450, value=valor_guardado("Frecuencia cardíaca")),
                ft.TextField(label="Frecuencia respiratoria (rpm)", width=450, value=valor_guardado("Frecuencia respiratoria")),
                ft.TextField(label="Tensión arterial (mmHg)", width=450, value=valor_guardado("Tensión arterial")),
                ft.TextField(label="Temperatura (°C)", width=450, value=valor_guardado("Temperatura")),
                ft.TextField(label="Examen Fisico", multiline=True, width=450, value=valor_guardado("Examen Fisico")),
                ft.Divider(),
                ft.TextField(label="Analisis", width=450, value=valor_guardado("Analisis")),
                ft.TextField(label="Impresion DX", width=450, value=valor_guardado("Impresion DX")),
                ft.TextField(label="Tratamiento", width=450, value=valor_guardado("Tratamiento")),
            ])


        if campos_extra.page is not None:
            campos_extra.update()

    formato_dropdown.on_change = actualizar_campos_extra
    if historia_existente:
        actualizar_campos_extra(None)

    def guardar_click(ev):
        historia = {
            "formato": formato_dropdown.value or "Medicina General",
            "nombre": (nombre_input.value or "").strip(),
            "identificacion": (id_input.value or "").strip(),
            "estado civil": estado_civil_dropdown.value,
            "edad": edad_input.value,
            "sexo": sexo_dropdown.value,
            "hemoclasificacion": hemoclasificacion_dropdown.value,
            "escolaridad": escolaridad_dropdown.value,
            "ocupacion": ocupacion_input.value,
            "direccion": direccion_input.value,
            "acomp_parentesco": acomp_parentesco_dropdown.value,
            "acomp_nombre": acomp_nombre_input.value,
            "eps": eps_dropdown.value,
            "fuente_info": fuente_info_dropdown.value,
            "confianza_info": confianza_info_dropdown.value,
            "fecha_nacimiento": (fecha_nacimiento_input.value or "").strip(),
            "motivo": (motivo_input.value or "").strip(),
            "enfermedad actual": (enfermedadactual_input.value or "").strip(),
            "rev_sis": (rev_sis_input.value or "").strip(),
            "fecha": (fecha_input.value or "").strip(),
            "extra": {}
        }

        for campo in campos_extra.controls:
            if isinstance(campo, ft.TextField):
                historia["extra"][campo.label] = (campo.value or "").strip()

        historias = cargar_historias()
        if index is not None:
            historias[index] = historia
        else:
            historias.append(historia)
        guardar_todas_las_historias(historias)

        refrescar_lista()
        page.close(dialogo)
        page.snack_bar = ft.SnackBar(ft.Text("Historia guardada correctamente"), open=True)
        page.update()

    dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Historia Clínica" if historia_existente else "Nueva Historia Clínica"),
        content=ft.Container(
            width=450,
            height=450,
            content=ft.Column(
                controls=[
                    formato_dropdown,
                    ft.Row([boton_fecha_historia], alignment=ft.MainAxisAlignment.CENTER),
                    fecha_input,
                    nombre_input,
                    id_input,
                    estado_civil_dropdown,
                    ft.Row([boton_fecha], alignment=ft.MainAxisAlignment.CENTER),
                    fecha_nacimiento_input,
                    edad_input,
                    sexo_dropdown,
                    hemoclasificacion_dropdown,
                    escolaridad_dropdown,
                    ocupacion_input,
                    direccion_input,
                    acomp_parentesco_dropdown,
                    acomp_nombre_input,
                    eps_dropdown,
                    fuente_info_dropdown,
                    confianza_info_dropdown,
                    motivo_input,
                    enfermedadactual_input,
                    ft.Divider(),
                    rev_sis_input,
                    ft.Divider(),
                    campos_extra
                ],
                tight=True,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda ev: page.close(dialogo)),
            ft.TextButton("Guardar", on_click=guardar_click),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )


    page.dialog = dialogo
    page.open(dialogo)


def pantalla_historia_clinica(page: ft.Page):
    lista_panels = ft.ExpansionPanelList(expand_icon_color=ft.Colors.WHITE, elevation=8)

    def refrescar_lista():
        lista_panels.controls.clear()
        for idx, hist in enumerate(cargar_historias()):
            lista_panels.controls.append(_panel_de_historia(hist, idx, refrescar_lista, page))
        try:
            lista_panels.update()
        except AssertionError:
            pass

    refrescar_lista()

    encabezado = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(height=50),
                ft.Container(
                    content=ft.Text(
                        "Mi archivo clínico",
                        size=25,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        expand=True
                    ),
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ADD,
                        icon_color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE,
                        on_click=lambda e: mostrar_formulario_historia(page, refrescar_lista),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=100),
                            padding=10
                        ),
                        tooltip="Crear nueva historia",
                    ),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(16),
        margin=ft.margin.only(top=10, bottom=20),
        alignment=ft.alignment.center
    )

    return ft.Column(
        expand=True,
        controls=[
            encabezado,
            ft.Container(
                expand=True,
                content=ft.ListView(
                    expand=True,
                    controls=[lista_panels],
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                ),
            ),
        ],
    )
