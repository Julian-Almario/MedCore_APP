import flet as ft
from calculadoras.electrolitos import *
from calculadoras.mate import *
from calculadoras.general import *
from calculadoras.renal import *
from calculadoras.reumatologia import *
from calculadoras.infectologia import *
from calculadoras.ginecologia import *
from calculadoras.cardio import *
from calculadoras.abdomen import *


calculadoras = [
        {
            "titulo": "Indice de masa corporal",
            "tags": ["imc", "peso", "altura", "nutrición", "bmi"],
            "componente": imc()
        },
        {
            "titulo": "Regla de tres (Directa)",
            "tags": ["proporciones", "aritmética", "matemática"],
            "componente": regla_de_tres()
        },
        {
            "titulo": "Talla medio parental",
            "tags": ["crecimiento", "niños", "pediatría", "estatura", "genética"],
            "componente": talla_medioparental()
        },
        {
            "titulo": "TFG Ecuación de Schwartz 2009",
            "tags": ["nefrología", "función renal", "schwartz", "creatinina", "riñón"],
            "componente": tfg_schwartz()
        },
        {
            "titulo": "Criterios SLICC para diagnóstico de LES",
            "tags": ["lupus", "inmunologia", "criterios"],
            "componente": slicc_page()
        },
        {
            "titulo": "qSOFA (Sepsis)",
            "tags": ["sepsis", "adultos", "criterios"],
            "componente": qsofa()
        },
        {
            "titulo": "Sofa Score (Sepsis)",
            "tags": ["sepsis", "adultos", "criterios"],
            "componente": sofa_score()
        },
        {
            "titulo": "CKD-EPI 2021",
            "tags": ["nefrología", "función renal", "creatinina", "eGFR","adultos"],
            "componente": ckd_epi_2021()
        },
        {
            "titulo": "Anion Gap",
            "tags": ["bioquímica", "electrolitos", "ácido-base", "anion gap"],
            "componente": calculadora_anion_gap()
        },
        {
            "titulo": "Sodio corregido",
            "tags": ["bioquímica", "electrolitos", "hiperglucemia", "sodio"],
            "componente": sodio_corregido()
        },
        {
            "titulo": "Edad gestaional FUM",
            "tags": ["ginecologia", "pediatria"],
            "componente": edad_gestacional_fur()
        },
        {
            "titulo": "Edad prematura corregida",
            "tags": ["ginecologia", "pediatria"],
            "componente": edad_corregida_prematuro()
        },
        {
            "titulo": "Presion arterial media (PAM)",
            "tags": ["cardiología", "presión arterial", "PAM"],
            "componente": presion_arterial_media()
        },
        {
            "titulo": "Criterios de Wells para TVP",
            "tags": ["trombosis", "venosa", "criterios", "wells"],
            "componente": criterios_wells_tvp()
        },
        {
            "titulo": "Criterios de Wells para TEP",
            "tags": ["tromboembolismo", "pulmonar", "criterios", "wells"],
            "componente": criterios_wells_tep()
        },
        {
            "titulo": "Criterios de Alvarado para Apendicitis",
            "tags": ["apendicitis", "quirúrgica", "criterios", "alvarado"],
            "componente": criterios_alvarado()
        },
        {
            "titulo": "Indice de bishop",
            "tags": ["ginecolgia", "quirúrgica", "parto", "borramiento"],
            "componente": bishop()
        }
    ]