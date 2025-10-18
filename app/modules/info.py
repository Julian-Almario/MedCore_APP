import os
import requests
import flet as ft
import tempfile
import shutil

RUTA_MDS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "data", "guias"))
RUTA_ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "anexos"))
BACKEND_URL = "http://localhost:8000"

def descargar_md_desde_backend(page: ft.Page, show_dialog: bool = True):
    try:
        # Asegurar que la carpeta exista
        os.makedirs(RUTA_MDS, exist_ok=True)

        # Solicitar lista de perlas al backend (si falla aquí, no tocamos nada)
        resp = requests.get(f"{BACKEND_URL}/pearls", timeout=10)
        resp.raise_for_status()
        archivos = resp.json().get("pearls", [])
        if not archivos:
            msg = "El servidor no reportó perlas para descargar."
            if show_dialog:
                dlg_info = ft.AlertDialog(
                    title=ft.Text("Sin perlas en servidor"),
                    content=ft.Text(msg),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_info))],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog = dlg_info
                page.open(dlg_info)
            return {"success": True, "descargados": 0, "borrados": 0, "message": msg}

        # Descargar a un directorio temporal; si falla, no se toca RUTA_MDS
        tmpdir = tempfile.mkdtemp()
        descargados = 0
        try:
            for archivo in archivos:
                archivo_url = f"{BACKEND_URL}/pearls/{archivo}"
                r = requests.get(archivo_url, timeout=15)
                r.raise_for_status()
                destino_tmp = os.path.join(tmpdir, archivo)
                with open(destino_tmp, "w", encoding="utf-8") as f:
                    f.write(r.text)
                descargados += 1
        except Exception as ex:
            shutil.rmtree(tmpdir, ignore_errors=True)
            msg = f"Ocurrió un error al descargar las perlas: {str(ex)}"
            if show_dialog:
                dlg_error = ft.AlertDialog(
                    title=ft.Text("Error de descarga"),
                    content=ft.Text(msg),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_error))],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog = dlg_error
                page.open(dlg_error)
            return {"success": False, "message": str(ex)}

        # Si llegamos aquí, las descargas fueron exitosas: aplicar cambios en RUTA_MDS
        removed_count = 0
        try:
            local_files = set(os.listdir(RUTA_MDS)) if os.path.exists(RUTA_MDS) else set()
            remote_files = set(archivos)
            # eliminar locales que ya no están en remoto (solo .md)
            for nombre in local_files - remote_files:
                ruta = os.path.join(RUTA_MDS, nombre)
                if os.path.isfile(ruta) and nombre.lower().endswith(".md"):
                    try:
                        os.remove(ruta)
                        removed_count += 1
                    except Exception:
                        pass
            # mover los nuevos descargados desde tmpdir a RUTA_MDS
            for nombre in os.listdir(tmpdir):
                shutil.move(os.path.join(tmpdir, nombre), os.path.join(RUTA_MDS, nombre))
            msg = f"Perlas: descargadas={descargados}, eliminadas_previas={removed_count}"
            if show_dialog:
                dlg_exito = ft.AlertDialog(
                    title=ft.Text("Actualización completada"),
                    content=ft.Text(msg),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_exito))],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog = dlg_exito
                page.open(dlg_exito)
            try:
                page.update()
            except Exception:
                pass
            return {"success": True, "descargados": descargados, "borrados": removed_count, "message": msg}
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    except Exception as ex:
        if show_dialog:
            dlg_error = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"Ocurrió un error al actualizar: {str(ex)}"),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_error))],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dlg_error
            page.open(dlg_error)
        return {"success": False, "message": str(ex)}

def info_page(page: ft.Page):

    def web(e):
        page.launch_url("https://www.julianalmario.social/")

    def repo(e):
        page.launch_url("https://github.com/Julian-Almario/MedCore_APP")


    my_web = ft.GestureDetector(
        content=ft.Image(src="../assets/myweb.png", width=150, height=50),
        on_tap=web,
    )

    repo_project = ft.GestureDetector(
        content=ft.Image(src="../assets/repository.png", width=150, height=50),
        on_tap=repo,
    )


    images_row = ft.Row(
        controls=[my_web, repo_project],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )
    
    #Informacion del desarrollo
    creador_info = ft.Column(
        controls=[
            ft.Text("Created by Julian Almario Loaiza", size=18),
            images_row,
            ft.Text("Versión: 1.0.0 (Octubre 2025)", size=14, color=ft.Colors.OUTLINE),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Lista de referencias
    referencias = [
        "- Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315(8):801–810. doi:10.1001/jama.2016.0287",
        "- Charles K, Lewis MJ, Montgomery E, Reid M. The 2021 Chronic Kidney Disease Epidemiology Collaboration Race-Free Estimated Glomerular Filtration Rate Equations in Kidney Disease: Leading the Way in Ending Disparities. Health Equity. 2024 Jan 12;8(1):39-45. doi: 10.1089/heq.2023.0038. PMID: 38250300; PMCID: PMC10797164.",
        "- Ohle R, O'Reilly F, O'Brien KK, Fahey T, Dimitrov BD. The Alvarado score for predicting acute appendicitis: a systematic review. BMC Med. 2011 Dec 28;9:139. doi: 10.1186/1741-7015-9-139. PMID: 22204638; PMCID: PMC3299622.",
        "- Singh, S., & Goel, A. (2023). A study of modified Wells score for pulmonary embolism and age-adjusted D-dimer values in patients at risk for deep venous thrombosis. Journal of Family Medicine and Primary Care, 12(9), 2020-2023. https://doi.org/10.4103/jfmpc.jfmpc_2455_22",
        "- Pandey, D. G., & Sharma, S. (2023). Biochemistry, Anion Gap. En StatPearls [Internet]. StatPearls Publishing. https://www.ncbi.nlm.nih.gov/books/NBK539757/",
        "- Petri, M., Orbai, A.-M., Alarcón, G. S., Gordon, C., Merrill, J. T., Fortin, P. R., Bruce, I. N., Isenberg, D., Wallace, D. J., Nived, O., Sturfelt, G., Ramsey-Goldman, R., Bae, S.-C., Hanly, J. G., Sanchez-Guerrero, J., Clarke, A., Aranow, C., Manzi, S., Urowitz, M., … Magder, L. S. (2012). Derivation and Validation of Systemic Lupus International Collaborating Clinics Classification Criteria for Systemic Lupus Erythematosus. Arthritis and rheumatism, 64(8), 2677-2686. https://doi.org/10.1002/art.34473",
        "- Edad corregida para bebés prematuros. (2018, diciembre 15). HealthyChildren.org. https://www.healthychildren.org/Spanish/ages-stages/baby/preemie/Paginas/Corrected-Age-For-Preemies.aspx",
        "- Hillier, T. A., Abbott, R. D., & Barrett, E. J. (1999). Hyponatremia: Evaluating the correction factor for hyperglycemia. The American Journal of Medicine, 106(4), 399-403. https://doi.org/10.1016/s0002-9343(99)00055-8",
        "- Peres Bota, D., Mélot, C., Lopes Ferreira, F., & Vincent, J.-L. (2003). Infection Probability Score (IPS): A method to help assess the probability of infection in critically ill patients. Critical Care Medicine, 31(11), 2579-2584. https://doi.org/10.1097/01.CCM.0000094223.92746.56",
        "- New Creatinine- and Cystatin C–Based Equations to Estimate GFR without Race | New England Journal of Medicine. (s. f.). Recuperado 17 de octubre de 2025, de https://www.nejm.org/doi/full/10.1056/NEJMoa2102953",
        "- Schwartz, G. J., Muñoz, A., Schneider, M. F., Mak, R. H., Kaskel, F., Warady, B. A., & Furth, S. L. (2009). New equations to estimate GFR in children with CKD. Journal of the American Society of Nephrology: JASN, 20(3), 629-637. https://doi.org/10.1681/ASN.2008030287",
        "- Bishop, E. H. (1964). PELVIC SCORING FOR ELECTIVE INDUCTION. Obstetrics and Gynecology, 24, 266-268.",
        "- Churpek, M. M., Snyder, A., Han, X., Sokol, S., Pettit, N., Howell, M. D., & Edelson, D. P. (2017). Quick Sepsis-related Organ Failure Assessment, Systemic Inflammatory Response Syndrome, and Early Warning Scores for Detecting Clinical Deterioration in Infected Patients outside the Intensive Care Unit. American Journal of Respiratory and Critical Care Medicine, 195(7), 906-911. https://doi.org/10.1164/rccm.201604-0854OC",
        "- Modi, S., Deisler, R., Gozel, K., Reicks, P., Irwin, E., Brunsvold, M., Banton, K., & Beilman, G. J. (2016). Wells criteria for DVT is a reliable clinical tool to assess the risk of deep venous thrombosis in trauma patients. World Journal of Emergency Surgery : WJES, 11, 24. https://doi.org/10.1186/s13017-016-0078-1"  
    ]

    # Informacion de referencias, terminos y condiciones, y privacidad
    info_panel = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.WHITE,
        elevation=8,
        divider_color=ft.Colors.WHITE,
        controls=[
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.MENU_BOOK, size=20),
                        ft.Text("Referencias bibliográficas", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Column(
                        controls=[ft.Text(ref, size=14) for ref in referencias],
                        spacing=6
                    ),
                    padding=ft.padding.all(20)
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.GAVEL, size=20),
                        ft.Text("Términos de uso y condiciones", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Text(
                        "La información médica contenida en esta aplicación ha sido recopilada cuidadosamente con fines educativos y de apoyo clínico. "
                        "No obstante, el uso que se le dé a esta información es responsabilidad exclusiva del usuario. "
                        "MedCore no reemplaza el juicio clínico profesional ni la consulta médica especializada.\n\n"
                        "El usuario acepta que cualquier decisión tomada con base en los datos proporcionados por la app es de su entera responsabilidad.",
                        size=14,
                        text_align=ft.TextAlign.LEFT,
                    ),
                    padding=ft.padding.all(20),
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
            ft.ExpansionPanel(
                header=ft.ListTile(
                    title=ft.Row([
                        ft.Icon(name=ft.Icons.LOCK, size=20),
                        ft.Text("Tratamiento de datos y privacidad", text_align=ft.TextAlign.LEFT),
                    ])
                ),
                content=ft.Container(
                    content=ft.Text(
                        "MedCore no recopila, transmite ni almacena información en servidores externos. "
                        "Toda la información ingresada, incluyendo historias clínicas, se guarda de manera local en el dispositivo del usuario.\n\n"
                        "Se recuerda que la historia clínica es un documento legal, privado y reservado. "
                        "Esta app fue diseñada únicamente como herramienta de organización de información médica para uso personal o profesional del usuario. "
                        "El manejo responsable y ético de los datos es esencial.",
                        size=14,
                        text_align=ft.TextAlign.LEFT,
                    ),
                    padding=ft.padding.all(20),
                ),
                expanded=False,
                bgcolor=ft.Colors.BLUE_GREY_900,
            ),
        ]
    )

    def actualizar_bases(e):
        # Ejecutar ambas actualizaciones en modo silencioso (sin diálogos individuales)
        res_md = {"success": False, "message": "No ejecutado"}
        res_img = {"success": False, "message": "No ejecutado"}
        try:
            res_md = descargar_md_desde_backend(page, show_dialog=False)
        except Exception as ex:
            res_md = {"success": False, "message": str(ex)}
        try:
            res_img = descargar_imagenes_desde_backend(page, on_update=lambda: page.update(), show_dialog=False)
        except Exception as ex:
            res_img = {"success": False, "message": str(ex)}

        # Construir un único diálogo resumen
        lines = []
        success = res_md.get("success", False) and res_img.get("success", False)
        title = "Actualización completada" if success else "Fallo en la conexión con el servidor"

        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text("\n".join(lines)),
            actions=[ft.TextButton("Cerrar", on_click=lambda ev: page.close(dlg))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg
        page.open(dlg)

    btn_actualizar = ft.ElevatedButton(
        text="Actualizar Bases de datos",
        icon=ft.Icons.AUTORENEW,
        icon_color=ft.Colors.BLUE_400,
        on_click=actualizar_bases,
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
    )

    # Vista principal de información
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        controls=[
            ft.Container(height=20),
            ft.Container(content=creador_info),
            ft.Row([btn_actualizar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=ft.Divider(thickness=1)),
            ft.Container(content=info_panel, padding=ft.padding.symmetric(horizontal=20)),
        ],
    )

def descargar_imagenes_desde_backend(page: ft.Page, on_update: callable = None, show_dialog: bool = True):
    try:
        os.makedirs(RUTA_ASSETS, exist_ok=True)
        resp = requests.get(f"{BACKEND_URL}/imagenes", timeout=10)
        resp.raise_for_status()
        archivos = resp.json().get("imagenes", [])
    except Exception as ex:
        msg = "No se pudo obtener la lista de imágenes. No se modificaron los assets."
        if show_dialog:
            dlg_error = ft.AlertDialog(
                title=ft.Text("Error de conexión"),
                content=ft.Text(msg),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_error))],
                modal=True,
            )
            page.open(dlg_error)
        return {"success": False, "message": str(ex) if ex else msg}

    if not archivos:
        msg = "El servidor no reportó imágenes para descargar."
        if show_dialog:
            dlg_info = ft.AlertDialog(
                title=ft.Text("Sin imágenes en servidor"),
                content=ft.Text(msg),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_info))],
                modal=True,
            )
            page.open(dlg_info)
        return {"success": True, "descargados": 0, "removed": 0, "message": msg}

    descargados = 0
    # Usar mkdtemp para mantener los archivos hasta confirmar la operación
    tmpdir = tempfile.mkdtemp()
    try:
        try:
            for archivo in archivos:
                url = f"{BACKEND_URL}/imagenes/{archivo}"
                r = requests.get(url, timeout=15, stream=True)
                r.raise_for_status()
                destino_tmp = os.path.join(tmpdir, archivo)
                with open(destino_tmp, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                descargados += 1
        except Exception:
            shutil.rmtree(tmpdir, ignore_errors=True)
            msg = "Ocurrió un error al descargar las imágenes. No se modificaron los assets."
            if show_dialog:
                dlg_error = ft.AlertDialog(
                    title=ft.Text("Error de descarga"),
                    content=ft.Text(msg),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_error))],
                    modal=True,
                )
                page.open(dlg_error)
            return {"success": False, "message": msg}

        # Confirmación antes de reemplazar los assets locales
        # Si show_dialog es False, aplicar la actualización automáticamente y devolver resultado
        try:
            local_files = set(os.listdir(RUTA_ASSETS)) if os.path.exists(RUTA_ASSETS) else set()
            remote_files = set(archivos)
            to_remove = local_files - remote_files
            removed_count = 0
            for nombre in to_remove:
                ruta = os.path.join(RUTA_ASSETS, nombre)
                if os.path.isfile(ruta):
                    try:
                        os.remove(ruta)
                        removed_count += 1
                    except Exception:
                        pass
            for nombre in os.listdir(tmpdir):
                shutil.move(os.path.join(tmpdir, nombre), os.path.join(RUTA_ASSETS, nombre))
            msg = f"Imágenes: descargadas={descargados}, eliminadas_locales={removed_count}"
            if show_dialog:
                dlg_exito = ft.AlertDialog(
                    title=ft.Text("Imágenes actualizadas"),
                    content=ft.Text(f"Se descargaron {descargados} imágenes y se actualizaron los assets."),
                    actions=[ft.TextButton("Cerrar", on_click=lambda ev: page.close(dlg_exito))],
                    modal=True,
                )
                page.open(dlg_exito)
            try:
                page.update()
                if on_update:
                    on_update()
            except Exception:
                pass
            return {"success": True, "descargados": descargados, "removed": removed_count, "message": msg}
        except Exception:
            msg = "Se descargaron las imágenes pero no se pudieron mover a assets."
            if show_dialog:
                dlg_error = ft.AlertDialog(
                    title=ft.Text("Error al actualizar"),
                    content=ft.Text(msg),
                    actions=[ft.TextButton("Cerrar", on_click=lambda ev: page.close(dlg_error))],
                    modal=True,
                )
                page.open(dlg_error)
            return {"success": False, "message": msg}
    except Exception:
        shutil.rmtree(tmpdir, ignore_errors=True)
        dlg_error = ft.AlertDialog(
            title=ft.Text("Error inesperado"),
            content=ft.Text("Ocurrió un error inesperado durante la actualización de imágenes."),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_error))],
            modal=True,
        )
        page.open(dlg_error)
        return {"success": False, "message": "Error inesperado"}