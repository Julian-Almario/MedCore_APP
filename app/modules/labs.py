import flet as ft
from laboratorios.hemograma import *
from laboratorios.lcr import *
from laboratorios.uroanalisis import *

paraclinicos = [
        {
            "titulo": "Hemograma",
            "tags": ["hemoglobina", "hemograma"],
            "componente": hemograma_panel()
        },
        {
            "titulo": "Líquido cefalorraquídeo (LCR)",
            "tags": ["lcr", "líquido cefalorraquídeo", "análisis de lcr"],
            "componente": lcr_panel()
        },
        {
            "titulo": "Uroanalisis",
            "tags": ["uroanálisis", "orina", "examen de orina"],
            "componente": orina_panel()
        }
    ]