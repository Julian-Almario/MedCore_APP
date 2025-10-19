![Banner](img/banner.png)

<p align="center">
  <img src="https://img.shields.io/github/license/Julian-Almario/medcore_APP" />
  <img src="https://img.shields.io/github/issues/Julian-Almario/medcore_app" />
  <img src="https://img.shields.io/github/stars/Julian-Almario/MedCore_APP" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/flet-%F0%9F%90%8D-green" />
</p>

# MedCore

**MedCore** es una aplicación multiplataforma para **móvil, web y escritorio**, desarrollada en Python utilizando el framework [Flet](https://flet.dev).
Su objetivo es centralizar calculadoras clínicas, valores de laboratorio de referencia y otros recursos útiles en una plataforma **intuitiva, modular y eficiente**.

## Características

* **Uso inmediato sin necesidad de inicio de sesión**
* **Búsqueda interactiva** por nombre o etiquetas
* **Calculadoras médicas de uso frecuente**:

  * Índice de Masa Corporal (IMC)
  * Regla de Tres (Directa)
  * Talla diana parental
  * TFG (Ecuación de Schwartz 2009)
  * Criterios SLICC para LES
  * Puntajes qSOFA y SOFA (Sepsis)
  * CKD-EPI 2021
  * Brecha aniónica y sodio corregido
  * **¡Y más!**
* **Valores de referencia de laboratorio** organizados por edad y tipo de prueba
* **Creador de historias clínicas** con opciones de exportación y edición
* **Almacenamiento local** con acceso completo sin conexión
* **Interfaz moderna, fluida y adaptable**
* **Modo oscuro permanente**
* **Diseño modular y ampliable**

## Tecnologías utilizadas

* **Python 3.10+**
* **[Flet](https://flet.dev/)** – Framework para interfaces web y de escritorio
* **Arquitectura modular y escalable**

## Instalación y ejecución

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/Julian-Almario/medcore_app.git
   cd medcore_app/src
   ```
2. **Instala las dependencias:**

   ```bash
   pip install flet requests
   ```
3. **Ejecuta la aplicación:**

   ```bash
   python main.py
   ```

> **Nota:** Se recomienda el uso de un entorno virtual.

## Estructura del proyecto

```
MedCore/
├── app/
│   ├── modules/                 # Módulos y componentes
│   ├── assets/                  # Imágenes, íconos y anexos de guias
│   ├── storage/                 # Almacenamiento de las guias, notas y DB medicamentos
│   ├── calculadoras/            # Almacenamiento de calculadoras
│   └── main.py                  # Punto de entrada principal
│
├── backend/                     # Servidor de flak para descarga de guias
│   ├── guias/                   # Almacenamiento de guias
│   ├── imagenes/                # Almacenamiento de imagenes que usan las guias
│   ├── static/                  # HTML servidor
│   ├── app.py
│   ├── requirements.txt
│   └── vercel.json
│
├── README.md                # Documentación principal
├── LICENSE                  # Licencia
├── CODE_OF_CONDUCT.md       # Código de conducta
└── pyproject.toml           # Configuraciones de compilación
```

## Estado actual

* [x] Acceso completo sin conexión "Solo se necesita actualizar las perlas clinicas en caso de que las desees"
* Calculadoras médicas disponibles:

  * [x] Índice de Masa Corporal (IMC)
  * [x] Regla de Tres (Directa)
  * [x] Talla diana parental
  * [x] TFG – Ecuación de Schwartz 2009
  * [x] Criterios SLICC para diagnóstico de LES
  * [x] qSOFA (Sepsis)
  * [x] Puntaje SOFA (Sepsis)
  * [x] CKD-EPI 2021
  * [x] Brecha aniónica
  * [x] Sodio corregido
* [x] Base de datos de medicamentos
* [x] Editor de base de datos de medicamentos
* [x] Búsqueda interactiva
* [x] Creador de notas personales

## Objetivo

**MedCore** busca ser una herramienta de referencia para estudiantes de medicina, médicos generales, que buscan tener a mano todas las herramientas posibles en un solo lugar para un trabajo y un aprendizaje mas optimo.

## Contribuciones

¡Las contribuciones son bienvenidas!
Abre un [pull request](https://github.com/Julian-Almario/medcore_app/pulls).

En caso de que piense que haga falta una calculadora o que quieras una en especifico me los puedes dejar en un mensaje directo en mi perfil de [Instagram](https://www.instagram.com/julianalmario_/)

## Licencia

Este proyecto está publicado bajo la **GNU GPL v3**.
Consulta el archivo [`LICENSE`](LICENSE) para más detalles.


*Inspirado en mi propia necesidad de contar con herramientas médicas en una sola aplicación.*