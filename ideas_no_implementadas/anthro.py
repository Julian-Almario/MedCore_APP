import flet as ft
import os
import json
from datetime import date, datetime
from modules.colors import *

RUTA_JSON_PESO_EDAD = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "storage", "data", "zscores", "peso-edad.json")
)
RUTA_JSON_PESO_TALLA = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "storage", "data", "zscores", "peso-talla.json")
)

with open(RUTA_JSON_PESO_EDAD, "r", encoding="utf-8") as f:
    DATA_PE = json.load(f)

OMS_GIRLS_WEEKS_PE  = {int(k): v for k, v in DATA_PE["girls"]["weeks"].items()}
OMS_GIRLS_MONTHS_PE = {int(k): v for k, v in DATA_PE["girls"]["months"].items()}
OMS_BOYS_WEEKS_PE   = {int(k): v for k, v in DATA_PE["boys"]["weeks"].items()}
OMS_BOYS_MONTHS_PE  = {int(k): v for k, v in DATA_PE["boys"]["months"].items()}

with open(RUTA_JSON_PESO_TALLA, "r", encoding="utf-8") as f:
    DATA_PT = json.load(f)

OMS_GIRLS_PESO_TALLA = {float(k): v for k, v in DATA_PT["girls"].items()}
OMS_BOYS_PESO_TALLA = {float(k): v for k, v in DATA_PT["boys"].items()}

def zscore_lms(value, L, M, S):
    if L == 0:
        return (value / M - 1) / S
    return ((value / M) ** L - 1) / (L * S)

def calcular_z_peso_edad(sexo: str, edad: int, peso: float, unidad: str):
    if sexo == "girl":
        tabla = OMS_GIRLS_WEEKS_PE if unidad == "sem" else OMS_GIRLS_MONTHS_PE
    else:
        tabla = OMS_BOYS_WEEKS_PE if unidad == "sem" else OMS_BOYS_MONTHS_PE

    if edad not in tabla:
        return None

    L = tabla[edad]["L"]
    M = tabla[edad]["M"]
    S = tabla[edad]["S"]
    return zscore_lms(peso, L, M, S)

def calcular_z_peso_talla(sexo: str, talla: float, peso: float):
    if sexo == "girl":
        tabla = OMS_GIRLS_PESO_TALLA
    else:
        tabla = OMS_BOYS_PESO_TALLA
    
    talla_redondeada = round(talla, 1)

    if talla_redondeada not in tabla:
        return None

    L = tabla[talla_redondeada]["L"]
    M = tabla[talla_redondeada]["M"]
    S = tabla[talla_redondeada]["S"]
    
    return zscore_lms(peso, L, M, S)

def interpretar_z(z):
    if z is None:
        return "Fuera de rango"
    if z < -3:
        return "Desnutrición severa"
    if -3 <= z < -2:
        return "Desnutrición moderada"
    if -2 <= z <= 2:
        return "Normal"
    if 2 < z <= 3:
        return "Sobrepeso"
    return "Obesidad"

def calcular_edad_semanas_meses(fecha_str: str):
    try:
        fnac = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        hoy = date.today()
        dias = (hoy - fnac).days
        if dias < 0:
            return None, None
        semanas = dias // 7
        if dias <= 91:
            return semanas, "sem"
        
        meses_completos = int(dias // 30.4375)
        
        if 0 < meses_completos <= 60:
             return meses_completos, "mes"
        
        return None, None
    except ValueError:
        return None, None

def show_anthropometry():
    fecha_texto = ft.Text("Fecha de nacimiento: -", color=TEXT_COLOR)
    # Resultado ahora contendrá todos los índices (P/E, T/E, P/T)
    resultado = ft.Text("", size=16, color=TEXT_COLOR)

    date_picker_ref = ft.Ref[ft.DatePicker]()
    
    # Campo para el peso
    peso_input = ft.TextField(
        label="Peso (kg)", 
        width=220, 
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    # Campo para la altura/talla
    altura_input = ft.TextField(
        label="Talla/Longitud (cm)",
        width=220, 
        keyboard_type=ft.KeyboardType.NUMBER
    )

    sexo_dropdown = ft.Dropdown(
        label="Sexo",
        width=220,
        value="girl",
        options=[
            ft.dropdown.Option("girl"),
            ft.dropdown.Option("boy")
        ]
    )

    edad_calculada = {"edad": None, "unidad": None}

    def on_fnac_selected(e):
        if e.data:
            fnac = datetime.fromisoformat(e.data).strftime("%Y-%m-%d")
            edad, unidad = calcular_edad_semanas_meses(fnac)
            edad_calculada["edad"] = edad
            edad_calculada["unidad"] = unidad
            if edad is None:
                fecha_texto.value = "Fecha inválida o edad fuera de rango (0-60 meses)"
            else:
                fecha_texto.value = f"Edad: {edad} {'semanas' if unidad == 'sem' else 'meses'}"
        else:
            edad_calculada["edad"] = None
            edad_calculada["unidad"] = None
            fecha_texto.value = "Fecha de nacimiento: -"
        fecha_texto.update()

    date_picker = ft.DatePicker(ref=date_picker_ref, on_change=on_fnac_selected)

    def abrir_date_picker(e):
        e.page.dialog = date_picker_ref.current
        date_picker_ref.current.open = True
        e.page.update()


    def calcular(e):
        try:
            peso = float(peso_input.value)
        except Exception:
            peso = None
        
        try:
            altura = float(altura_input.value)
        except Exception:
            altura = None


        edad = edad_calculada["edad"]
        unidad = edad_calculada["unidad"]
        
        if edad is None:
            resultado.value = "Selecciona una fecha válida"
            resultado.update()
            return
        
        sexo = sexo_dropdown.value
        
        resultado_pe = ""
        if peso is not None:
            z_pe = calcular_z_peso_edad(sexo, edad, peso, unidad)
            if z_pe is None:
                resultado_pe = "P/E: Fuera de rango para la edad"
            else:
                dx_pe = interpretar_z(z_pe)
                resultado_pe = f"**P/E** Z-score: {z_pe:.2f}\nDiagnóstico: {dx_pe}"
        else:
            resultado_pe = "P/E: Peso no ingresado"


        resultado_te_pt = "\n---\n"
        if altura is None:
             resultado_te_pt += "Talla/Longitud no ingresada. No se calculan T/E ni P/T."
        else:
            talla_cm = altura
            talla_m = altura / 100
            z_pt = calcular_z_peso_talla(sexo, talla_cm, peso)

        if z_pt is None:
            resultado_te_pt += "P/T: Fuera de rango para la talla\n"
        else:
            dx_pt = interpretar_z(z_pt)
            resultado_te_pt += f"**P/T** Z-score: {z_pt:.2f}\nDiagnóstico: {dx_pt}\n"

            resultado_te_pt += "\nT/E: Aún no implementado (faltan tablas OMS T/E)"



        # Mostrar el resultado final
        resultado.value = f"{resultado_pe}{resultado_te_pt}"
        resultado.update()

    contenido = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        expand=False,
        controls=[
            ft.Text(
                "Antropometría OMS",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=TEXT_COLOR,
                text_align=ft.TextAlign.CENTER
            ),

            ft.ElevatedButton(
                "Seleccionar fecha de nacimiento",
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=abrir_date_picker
            ),

            fecha_texto,

            sexo_dropdown,
            
            
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    peso_input,
                    altura_input, 
                ]
            ),
            
            ft.ElevatedButton("Calcular", on_click=calcular),

            ft.Container(
                content=resultado,
                padding=14,
                margin=ft.margin.only(top=8),
                border_radius=10,
                bgcolor=PRIMARY_COLOR,
                alignment=ft.alignment.center_left,
                width=320
            ),

            date_picker
        ]
    )

    return ft.Container(
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.symmetric(vertical=30, horizontal=20),
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[contenido]
        )
    )
