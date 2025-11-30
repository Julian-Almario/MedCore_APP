# modules/anthro.py
import flet as ft
import os
import json
from datetime import date, datetime
from modules.colors import *   # mantiene tu paleta

RUTA_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "storage", "data", "zscores", "girlzscore.json")
)

with open(RUTA_JSON, "r", encoding="utf-8") as f:
    DATA = json.load(f)

# Convertir claves string -> int
OMS_GIRLS_WEEKS  = {int(k): v for k, v in DATA["girls"]["weeks"].items()}
OMS_GIRLS_MONTHS = {int(k): v for k, v in DATA["girls"]["months"].items()}
OMS_BOYS_WEEKS   = {int(k): v for k, v in DATA["boys"]["weeks"].items()}
OMS_BOYS_MONTHS  = {int(k): v for k, v in DATA["boys"]["months"].items()}

def zscore_lms(value, L, M, S):
    if L == 0:
        return (value / M - 1) / S
    return ((value / M) ** L - 1) / (L * S)

def calcular_z_peso_edad(sexo: str, edad: int, peso: float, unidad: str):
    if sexo == "girl":
        tabla = OMS_GIRLS_WEEKS if unidad == "sem" else OMS_GIRLS_MONTHS
    else:
        tabla = OMS_BOYS_WEEKS if unidad == "sem" else OMS_BOYS_MONTHS

    if edad not in tabla:
        return None

    L = tabla[edad]["L"]
    M = tabla[edad]["M"]
    S = tabla[edad]["S"]
    return zscore_lms(peso, L, M, S)

def interpretar_z(z):
    if z is None:
        return "Datos incompletos"
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
        if semanas <= 13:
            return semanas, "sem"
        meses = dias // 30
        return meses, "mes"
    except Exception:
        return None, None

def show_anthropometry():
    fecha_texto = ft.Text("Fecha de nacimiento: -", color=TEXT_COLOR)
    resultado = ft.Text("", size=16, color=TEXT_COLOR)

    date_picker_ref = ft.Ref[ft.DatePicker]()
    peso_input = ft.TextField(label="Peso (kg)", width=220, keyboard_type=ft.KeyboardType.NUMBER)

    # sexo dropdown dentro del scope de la vista
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

    # DatePicker y calculo de edad
    def on_fnac_selected(e):
        if e.data:
            fnac = datetime.fromisoformat(e.data).strftime("%Y-%m-%d")
            edad, unidad = calcular_edad_semanas_meses(fnac)
            edad_calculada["edad"] = edad
            edad_calculada["unidad"] = unidad
            if edad is None:
                fecha_texto.value = "Fecha inválida"
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

    # Handler calcular
    def calcular(e):
        try:
            peso = float(peso_input.value)
        except Exception:
            resultado.value = "Error: peso inválido"
            resultado.update()
            return

        edad = edad_calculada["edad"]
        unidad = edad_calculada["unidad"]
        if edad is None:
            resultado.value = "Selecciona una fecha válida"
            resultado.update()
            return

        sexo = sexo_dropdown.value  # "girl" o "boy"
        z = calcular_z_peso_edad(sexo, edad, peso, unidad)
        if z is None:
            resultado.value = "Edad fuera del rango OMS (0–13 semanas / 0–60 meses)"
            resultado.update()
            return

        dx = interpretar_z(z)
        resultado.value = f"Z-score: {z:.2f}\nDiagnóstico: {dx}"
        resultado.update()

    contenido = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=18,
        expand=False,
        controls=[
            ft.Text(
                "Antropometría OMS — Peso para la edad",
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

            peso_input,

            ft.ElevatedButton("Calcular", on_click=calcular),

            ft.Container(
                content=resultado,
                padding=14,
                margin=ft.margin.only(top=8),
                border_radius=10,
                bgcolor=PRIMARY_COLOR,
                alignment=ft.alignment.center,
                width=320
            ),

            date_picker
        ]
    )

    # Envolver en un container expandible centrado horizontalmente
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

