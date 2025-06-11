![Banner](img/banner.png)

<p align="center">
  <img src="https://img.shields.io/github/license/Julian-Almario/medcore_APP" />
  <img src="https://img.shields.io/github/issues/Julian-Almario/medcore_app" />
  <img src="https://img.shields.io/github/stars/Julian-Almario/MedCore_APP" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/flet-%F0%9F%90%8D-green" />
</p>

# MedCore

**MedCore** es una aplicación multiplataforma para **móviles, web y escritorio**, desarrollada en Python utilizando el framework [Flet](https://flet.dev). Su objetivo es centralizar calculadoras clínicas, valores de referencia paraclínicos y otros recursos útiles en una plataforma intuitiva, modular y eficiente.

---

## 🎬 Demo

<p align="center">
  <img src="img/demo.gif" alt="Demo MedCore" width="400"/>
</p>

---

## 🩺 Características

- 🚀 **Uso inmediato sin necesidad de inicio de sesión**
- 🔎 **Búsqueda interactiva** por nombre o etiquetas
- 🧮 **Calculadoras médicas** de uso frecuente:
  - Índice de masa corporal (IMC)
  - Regla de tres (Directa)
  - Talla medio parental
  - TFG (Schwartz 2009)
  - Criterios SLICC para LES
  - qSOFA y SOFA Score (Sepsis)
  - CKD-EPI 2021
  - Anion Gap y Sodio corregido
  - **¡Y más!**
- 🧪 **Valores normales paraclínicos** organizados por edad y tipo de análisis
- 📝 **Creador de historias clínicas** con exportación y edición
- 📦 **Almacenamiento local** y acceso offline completo
- 💻 **Interfaz moderna, fluida y responsiva**
- 🌙 **Modo oscuro permanente**
- 🧩 **Diseño modular** y expansible

---

## 🧰 Tecnologías utilizadas

- **Python 3.10+**
- **[Flet](https://flet.dev/)** – Framework para interfaces web y de escritorio
- **Arquitectura modular** y escalable

---

## 🚀 Instalación y ejecución

1. **Clona el repositorio:**
    ```bash
    git clone https://github.com/Julian-Almario/medcore_app.git
    cd medcore_app/src
    ```
2. **Instala las dependencias:**
    ```bash
    pip install flet
    ```
3. **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```
> **Nota:** Se recomienda usar un entorno virtual.

---

## 📁 Estructura del proyecto

```text
app/
│
├── main.py                  # Punto de entrada
├── README.md                # Documentación principal
├── LICENSE                  # Licencia
├── CODE_OF_CONDUCT.md       # Código de conducta
├── pyproject.toml           # Preferencias de Flet
├── app/
│   ├── modules/             # Módulos y componentes
│   └── assets/              # Imágenes e íconos
│
├── storage/
│   └── data/
│       ├── historias_clinicas/
│       └── meds.json
```

---

## 🧪 Estado actual

* [x] Acceso offline completo
* Valores de paraclínicos normales
    * [x] Hemograma
    * [x] LCR
    * [x] Uroanalisis
* Calculadoras médicas más usadas:
    * [x] Índice de masa corporal (IMC)
    * [x] Regla de tres (Directa)
    * [x] Talla medio parental
    * [x] TFG Ecuación de Schwartz 2009
    * [x] Criterios SLICC para diagnóstico de LES
    * [x] qSOFA (Sepsis)
    * [x] SOFA Score (Sepsis)
    * [x] CKD-EPI 2021
    * [x] Anion Gap
    * [x] Sodio corregido
* [x] Base de datos medicamentos
* [x] Búsqueda interactiva
* [x] Creador de historias clínicas

---

## 📌 Objetivo

**MedCore** busca ser una herramienta de referencia para estudiantes de medicina, médicos generales y especialistas, centralizando cálculos, valores normales y parámetros clave para agilizar la toma de decisiones clínicas.

---

## ❓ Preguntas frecuentes

**¿Puedo usar MedCore sin conexión a internet?**  
¡Sí! Todas las funciones principales son offline.

**¿Cómo reporto un bug o sugiero una mejora?**  
Abre un [issue aquí](https://github.com/Julian-Almario/medcore_app/issues).

---

## 🛠️ Soporte y contacto

¿Tienes dudas, sugerencias o necesitas soporte?  
📧 julian-andres-almario@hotmail.com  
O abre un [issue](https://github.com/Julian-Almario/medcore_app/issues).

---

## 🙌 Contribuciones

¡Las contribuciones son bienvenidas!  
Consulta la [guía de contribución](CONTRIBUTING.md) o abre un [pull request](https://github.com/Julian-Almario/medcore_app/pulls).

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **GNU GPL v3**.  
Consulta el archivo [`LICENSE`](LICENSE) para más detalles.

---

## 🌟 Reconocimientos

- Gracias a la comunidad de Flet y a todos los colaboradores.
- Inspirado por la necesidad de herramientas médicas accesibles y modernas.