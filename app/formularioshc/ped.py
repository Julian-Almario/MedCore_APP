import flet  as ft
from formularioshc.gene import *

campos.update({
    "hijo_de": ft.TextField(label="Hijo de"),
    "documento_ped": ft.TextField(label="Documento"),
    "episodio": ft.TextField(label="Episodio"),
    "edad_materna": ft.TextField(label="Edad materna"),
    "hemoclasificacion_ped": ft.TextField(label="Hemoclasificación"),
    "edad_gestacional": ft.TextField(label="Edad gestacional"),
    "fum": ft.TextField(label="FUM"),
    "gestaciones": ft.TextField(label="Gestaciones"),
    "controles_prenatales": ft.TextField(label="Controles prenatales"),
    "vacunacion": ft.TextField(label="Vacunación"),
    "ultima_ecografia": ft.TextField(label="Última ecografía"),
    "ag_shb": ft.TextField(label="Ag-SHB"),
    "vih": ft.TextField(label="VIH"),
    "prueba_no_treponemica": ft.TextField(label="Prueba no treponemica materna"),
    "prueba_treponemica": ft.TextField(label="Prueba treponemica materna"),
    "toxoplasma": ft.TextField(label="Toxoplasma"),
    "ptog": ft.TextField(label="PTOG"),
    "cultivo_estreptococo": ft.TextField(label="Cultivo rectovaginal para estreptococo B agalactiae"),
    "paraclinicos_maternos": ft.TextField(label="Paraclínicos maternos", multiline=True, max_lines=2),
    "ginecobstetricos": ft.TextField(label="Ginecobstetricos"),
    "patologicos_ped": ft.TextField(label="Patológicos"),
    "quirurgicos_ped": ft.TextField(label="Quirúrgicos"),
    "alergicos_ped": ft.TextField(label="Alérgicos"),
    "toxicos": ft.TextField(label="Tóxicos"),
    "farmacologicos": ft.TextField(label="Farmacológicos"),
    "familiares_ped": ft.TextField(label="Familiares"),
    "ruptura_membranas": ft.TextField(label="Ruptura de membranas"),
    "analgesia_epidural": ft.TextField(label="Analgesia epidural"),
    "medicamentos_ped": ft.TextField(label="Medicamentos"),
    "maduracion_fetal": ft.TextField(label="Maduración fetal"),
    "sexo_bebe": ft.TextField(label="Sexo del bebé"),
    "fecha_nacimiento_bebe": ft.TextField(label="Fecha de nacimiento"),
    "hora_nacimiento_bebe": ft.TextField(label="Hora de nacimiento"),
    "tipo_parto": ft.TextField(label="Tipo de parto"),
    "liquido_amniotico": ft.TextField(label="Líquido amniótico"),
    "adaptacion_neonatal": ft.TextField(label="Adaptación neonatal", multiline=True, max_lines=3),
    "apgar_minuto": ft.TextField(label="Apgar al minuto"),
    "apgar_5min": ft.TextField(label="Apgar a los 5 minutos"),
    "apgar_otros": ft.TextField(label="Apgar otros minutos"),
    "ballard": ft.TextField(label="Ballard (semanas)"),
    "peso_gramos": ft.TextField(label="Peso (g)"),
    "peso_percentil": ft.TextField(label="Peso (percentil)"),
    "talla_cm": ft.TextField(label="Talla (cm)"),
    "talla_percentil": ft.TextField(label="Talla (percentil)"),
    "pc_cm": ft.TextField(label="PC (cm)"),
    "pc_percentil": ft.TextField(label="PC (percentil)"),
    "pt_cm": ft.TextField(label="PT (cm)"),
    "pa_cm": ft.TextField(label="PA (cm)"),
    "diuresis": ft.TextField(label="Diuresis"),
    "meconio": ft.TextField(label="Meconio"),
    "diagnosticos_ped": ft.TextField(label="Diagnósticos", multiline=True, max_lines=2),
    "plan_ped": ft.TextField(label="Plan", multiline=True, max_lines=3),
})