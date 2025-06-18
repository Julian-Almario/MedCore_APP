import flet as ft
from laboratorios.hemograma import *
from laboratorios.lcr import *
from laboratorios.uroanalisis import *
from laboratorios.gineco import *

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
        },
        {
            "titulo": "Vaginitis Panel",
            "tags": ["vaginitis", "vaginosis", "candidiasis", "tricomoniasis", "vulvovaginitis"],
            "componente": vaginitis_panel()
        },
        {
            "titulo": "Flujo vaginal",
            "tags": ["ginecología", "flujo vaginal", "vaginitis"],
            "componente": flujo_vaginal_panel()
        }
    ]