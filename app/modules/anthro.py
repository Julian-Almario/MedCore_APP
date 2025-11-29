import flet as flet
import os
import json
from modules.colors import *


OMS_PESO_EDAD_F = {
    0:  {"L": 0.3809, "M": 3.2322, "S": 0.14171},
    1:  {"L": 0.1714, "M": 4.1873, "S": 0.13724},
    2:  {"L": 0.0962, "M": 5.1282, "S": 0.13040},
    3:  {"L": 0.0402, "M": 5.8458, "S": 0.12678},
    4:  {"L": 0.0008, "M": 6.4237, "S": 0.12402},
    5:  {"L": -0.0304, "M": 6.8985, "S": 0.12181},
    6:  {"L": -0.0546, "M": 7.2970, "S": 0.12002},
    7:  {"L": -0.0734, "M": 7.6422, "S": 0.11852},
    8:  {"L": -0.0884, "M": 7.9487, "S": 0.11722},
    9:  {"L": -0.1007, "M": 8.2254, "S": 0.11609},
    10: {"L": -0.1108, "M": 8.4790, "S": 0.11510},
    11: {"L": -0.1191, "M": 8.7137, "S": 0.11422},
    12: {"L": -0.1260, "M": 8.9329, "S": 0.11343},
    13: {"L": -0.1317, "M": 9.1399, "S": 0.11271},
    14: {"L": -0.1364, "M": 9.3369, "S": 0.11205},
    15: {"L": -0.1403, "M": 9.5253, "S": 0.11145},
    16: {"L": -0.1435, "M": 9.7064, "S": 0.11089},
    17: {"L": -0.1461, "M": 9.8806, "S": 0.11037},
    18: {"L": -0.1483, "M": 10.0480, "S": 0.10988},
    19: {"L": -0.1501, "M": 10.2086, "S": 0.10943},
    20: {"L": -0.1516, "M": 10.3628, "S": 0.10900},
    21: {"L": -0.1528, "M": 10.5108, "S": 0.10860},
    22: {"L": -0.1537, "M": 10.6527, "S": 0.10822},
    23: {"L": -0.1545, "M": 10.7886, "S": 0.10786},
    24: {"L": -0.1550, "M": 10.9185, "S": 0.10752},
    25: {"L": -0.1554, "M": 11.0427, "S": 0.10719},
    26: {"L": -0.1556, "M": 11.1610, "S": 0.10688},
    27: {"L": -0.1557, "M": 11.2736, "S": 0.10658},
    28: {"L": -0.1557, "M": 11.3806, "S": 0.10630},
    29: {"L": -0.1555, "M": 11.4820, "S": 0.10603},
    30: {"L": -0.1553, "M": 11.5780, "S": 0.10577},
    31: {"L": -0.1549, "M": 11.6686, "S": 0.10552},
    32: {"L": -0.1545, "M": 11.7540, "S": 0.10529},
    33: {"L": -0.1540, "M": 11.8343, "S": 0.10506},
    34: {"L": -0.1534, "M": 11.9096, "S": 0.10485},
    35: {"L": -0.1528, "M": 11.9801, "S": 0.10464},
    36: {"L": -0.1521, "M": 12.0460, "S": 0.10445},
    37: {"L": -0.1514, "M": 12.1074, "S": 0.10426},
    38: {"L": -0.1506, "M": 12.1644, "S": 0.10409},
    39: {"L": -0.1497, "M": 12.2173, "S": 0.10392},
    40: {"L": -0.1488, "M": 12.2662, "S": 0.10376},
    41: {"L": -0.1479, "M": 12.3113, "S": 0.10360},
    42: {"L": -0.1469, "M": 12.3527, "S": 0.10345},
    43: {"L": -0.1459, "M": 12.3907, "S": 0.10331},
    44: {"L": -0.1449, "M": 12.4253, "S": 0.10317},
    45: {"L": -0.1438, "M": 12.4567, "S": 0.10304},
    46: {"L": -0.1427, "M": 12.4851, "S": 0.10291},
    47: {"L": -0.1416, "M": 12.5105, "S": 0.10278},
    48: {"L": -0.1405, "M": 12.5331, "S": 0.10266},
    49: {"L": -0.1393, "M": 12.5531, "S": 0.10255},
    50: {"L": -0.1381, "M": 12.5705, "S": 0.10244},
    51: {"L": -0.1369, "M": 12.5856, "S": 0.10233},
    52: {"L": -0.1357, "M": 12.5983, "S": 0.10223},
    53: {"L": -0.1344, "M": 12.6088, "S": 0.10213},
    54: {"L": -0.1332, "M": 12.6172, "S": 0.10204},
    55: {"L": -0.1319, "M": 12.6235, "S": 0.10195},
    56: {"L": -0.1306, "M": 12.6279, "S": 0.10186},
    57: {"L": -0.1293, "M": 12.6304, "S": 0.10178},
    58: {"L": -0.1280, "M": 12.6312, "S": 0.10170},
    59: {"L": -0.1267, "M": 12.6303, "S": 0.10162},
    60: {"L": -0.1254, "M": 12.6278, "S": 0.10155},
}


def calcular_z_peso_edad(edad_meses: int, peso: float):
    if edad_meses not in OMS_PESO_EDAD_F:
        return None

    L = OMS_PESO_EDAD_F[edad_meses]["L"]
    M = OMS_PESO_EDAD_F[edad_meses]["M"]
    S = OMS_PESO_EDAD_F[edad_meses]["S"]

    return ((peso / M) ** L - 1) / (L * S)

def interpretar_z(z: float):
    if z is None:
        return "Datos incompletos"

    if z < -3:
        return "Desnutrición severa"
    elif -3 <= z < -2:
        return "Desnutrición moderada"
    elif -2 <= z <= +2:
        return "Normal"
    elif z > 2:
        return "Sobrepeso"

def show_anthropometry():
    edad_input = ft.TextField(label="Edad (meses)", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    peso_input = ft.TextField(label="Peso (kg)", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    resultado = ft.Text("", size=18, color=TEXT_COLOR)

    def calcular(e):
        try:
            edad = int(edad_input.value)
            peso = float(peso_input.value)

            z = calcular_z_peso_edad(edad, peso)
            dx = interpretar_z(z)

            resultado.value = f"Z-score: {z:.2f}\nDiagnóstico: {dx}"
        except:
            resultado.value = "Error: completa todos los campos"

        edad_input.update()
        peso_input.update()
        resultado.update()

    return ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Antropometría OMS - Peso para la edad (Niñas 0–60 meses)",
                    size=20, weight=ft.FontWeight.BOLD),

            ft.Row([edad_input, peso_input], alignment=ft.MainAxisAlignment.CENTER),

            ft.ElevatedButton("Calcular", on_click=calcular),

            ft.Container(
                content=resultado,
                padding=20,
                margin=20,
                border_radius=12,
                bgcolor=PRIMARY_COLOR
            ),
        ]
    )

