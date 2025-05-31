import flet as ft


def on_fecha_change(e):
    valor = campos["fecha_historia"].value
    # Solo permite números y guiones, máximo 10 caracteres
    valor_filtrado = re.sub(r"[^\d-]", "", valor)[:10]
    # Detecta si el usuario está borrando
    if len(valor_filtrado) < len(getattr(on_fecha_change, "ultimo_valor", "")):
        # Si está borrando, no autocompleta guiones
        campos["fecha_historia"].value = valor_filtrado
    else:
        # Autocompleta los guiones solo al escribir
        if len(valor_filtrado) == 4 and not valor_filtrado.endswith("-"):
            valor_filtrado += "-"
        elif len(valor_filtrado) == 7 and valor_filtrado.count("-") == 1:
            valor_filtrado += "-"
        if len(valor_filtrado) > 4 and valor_filtrado[4] != "-":
            valor_filtrado = valor_filtrado[:4] + "-" + valor_filtrado[4:]
        if len(valor_filtrado) > 7 and valor_filtrado[7] != "-":
            valor_filtrado = valor_filtrado[:7] + "-" + valor_filtrado[7:]
        campos["fecha_historia"].value = valor_filtrado
    # Guarda el último valor para la próxima llamada
    on_fecha_change.ultimo_valor = campos["fecha_historia"].value
    page.update()

campos = {
        "documento": ft.TextField(label="Documento", expand=True),
        "cama": ft.TextField(label="Cama", expand=True),
        "fecha_historia": ft.TextField(
            label="Fecha historia",
            hint_text="YYYY-MM-DD",
            expand=True,
            on_change=on_fecha_change,
        ),
        "nombre": ft.TextField(label="Nombre y apellidos"),
        "estado_civil": ft.TextField(label="Estado civil"),
        "fecha_nacimiento": ft.TextField(label="Fecha de nacimiento",expand=True),
        "edad": ft.TextField(label="Edad", input_filter=ft.NumbersOnlyInputFilter(),expand=True),
        "sexo": ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("Masculino"),
                ft.dropdown.Option("Femenino"),
                ft.dropdown.Option("Otro"),
            ],
            expand=True,
        ),
        "hemoclasificacion": ft.Dropdown(
            label="Hemoclasificación",
            options=[
                ft.dropdown.Option("A+"),
                ft.dropdown.Option("A-"),
                ft.dropdown.Option("B+"),
                ft.dropdown.Option("B-"),
                ft.dropdown.Option("AB+"),
                ft.dropdown.Option("AB-"),
                ft.dropdown.Option("O+"),
                ft.dropdown.Option("O-"),
            ],
            expand=True,
        ),
        "ocupacion": ft.TextField(label="Ocupación"),
        "escolaridad": ft.TextField(label="Escolaridad"),
        "direccion": ft.TextField(label="Dirección y Lugar de residencia"),
        "nombre_acompanante": ft.TextField(label="Nombre Acompañante"),
        "parentesco_acompanante": ft.Dropdown(
            label="Parentesco del acompañante",
            options=[
                ft.dropdown.Option("Madre"),
                ft.dropdown.Option("Padre"),
                ft.dropdown.Option("Hijo/a"),
                ft.dropdown.Option("Esposo/a"),
                ft.dropdown.Option("Amigo"),
            ],
            expand=True,
        ),
        "fuente_info": ft.Dropdown(
            label="Confiabilidad",
            options=[
                ft.dropdown.Option("Buena"),
                ft.dropdown.Option("Aceptable"),
                ft.dropdown.Option("Baja"),
            ],
            expand=True,
        ),
        "eps": ft.TextField(label="EPS"),
        "motivo": ft.TextField(label="Motivo de consulta", multiline=True, max_lines=3),
        "enfermedad_actual": ft.TextField(label="Enfermedad actual", multiline=True, max_lines=10),

        # Antecedentes
        "patologicos": ft.TextField(label="Patológicos", multiline=True, max_lines=2),
        "infecciosos": ft.TextField(label="Infecciosos y no infecciosos", multiline=True, max_lines=2),
        "alergias": ft.TextField(label="Alergias", multiline=True, max_lines=2),
        "hospitalizaciones": ft.TextField(label="Hospitalizaciones previas", multiline=True, max_lines=2),
        "urgencias": ft.TextField(label="Consultas a urgencias", multiline=True, max_lines=2),
        "quirurgicos": ft.TextField(label="Quirúrgicos", multiline=True, max_lines=2),
        "transfusionales": ft.TextField(label="Transfusionales", multiline=True, max_lines=2),
        "traumaticos": ft.TextField(label="Traumáticos", multiline=True, max_lines=2),
        "zoo_contactos": ft.TextField(label="Zoo Contactos", multiline=True, max_lines=2),
        "epidemiologicos": ft.TextField(label="Epidemiológicos", multiline=True, max_lines=2),

        # No patológicos
        "prenatales": ft.TextField(label="Prenatales y perinatales", multiline=True, max_lines=2),
        "alimentacion": ft.TextField(label="Alimentación", multiline=True, max_lines=2),
        "crecimiento": ft.TextField(label="Crecimiento y desarrollo", multiline=True, max_lines=2),
        "inmunizaciones": ft.TextField(label="Inmunizaciones", multiline=True, max_lines=2),
        "sicosociales": ft.TextField(label="Sicosociales", multiline=True, max_lines=2),
        "escolaridad_no_pat": ft.TextField(label="Escolaridad (no patológicos)", multiline=True, max_lines=2),

        # Familiares
        "familiares_patologias": ft.TextField(label="Familiares - Patologías diagnosticadas", multiline=True, max_lines=2),
        "familiares_composicion": ft.TextField(label="Familiares - Composición familiar", multiline=True, max_lines=2),

        "revision_sistemas": ft.TextField(label="Revisión por sistemas", multiline=True, max_lines=4),

        # Examen físico
        "aspectos_generales": ft.TextField(label="Aspectos generales", multiline=True, max_lines=2),
        "signos_vitales": ft.TextField(label="Signos vitales (T, FC, FR, PA, SAO2, FIO2)", multiline=True, max_lines=2),
        "peso": ft.TextField(label="Peso/Kg", width=100),
        "talla": ft.TextField(label="Talla/Cm", width=100),
        "piel": ft.TextField(label="Piel", multiline=True, max_lines=2),
        "cabeza": ft.TextField(label="Cabeza", multiline=True, max_lines=2),
        "ojos": ft.TextField(label="Ojos", multiline=True, max_lines=2),
        "boca": ft.TextField(label="Boca", multiline=True, max_lines=2),
        "oidos": ft.TextField(label="Oidos", multiline=True, max_lines=2),
        "nariz": ft.TextField(label="Nariz", multiline=True, max_lines=2),
        "cuello": ft.TextField(label="Cuello", multiline=True, max_lines=2),
        "cardiopulmonar": ft.TextField(label="Cardiopulmonar", multiline=True, max_lines=2),
        "abdomen": ft.TextField(label="Abdomen", multiline=True, max_lines=2),
        "neuromuscular": ft.TextField(label="Neuromuscular", multiline=True, max_lines=2),
        "musculo_esqueletico": ft.TextField(label="Músculo esquelético", multiline=True, max_lines=2),
        "dx": ft.TextField(label="DX", multiline=True, max_lines=2),
        "analisis": ft.TextField(label="Analisis", multiline=True, max_lines=2),
        "plan_manejo": ft.TextField(label="Plan de manejo", multiline=True, max_lines=10),
        "t": ft.TextField(label="T", width=90),
        "fc": ft.TextField(label="FC", width=90),
        "fr": ft.TextField(label="FR", width=90),
        "pa": ft.TextField(label="PA", width=90),
        "sao2": ft.TextField(label="SAO2", width=90),
        "fio2": ft.TextField(label="FIO2", width=90),
    }