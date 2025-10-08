![Banner](img/banner.png)

<p align="center">
  <img src="https://img.shields.io/github/license/Julian-Almario/medcore_APP" />
  <img src="https://img.shields.io/github/issues/Julian-Almario/medcore_app" />
  <img src="https://img.shields.io/github/stars/Julian-Almario/MedCore_APP" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/flet-%F0%9F%90%8D-green" />
</p>

# MedCore

**MedCore** is a cross-platform application for **mobile, web, and desktop**, developed in Python using the [Flet](https://flet.dev) framework. Its goal is to centralize clinical calculators, reference lab values, and other useful resources in an intuitive, modular, and efficient platform.

## Demo

<p align="center">
  <img src="img/demo.gif" alt="MedCore Demo" width="400"/>
</p>

## Features

- **Immediate use without login**
- **Interactive search** by name or tags
- **Frequently used medical calculators**:
  - Body Mass Index (BMI)
  - Rule of Three (Direct)
  - Mid-parental height
  - GFR (Schwartz 2009)
  - SLICC criteria for SLE
  - qSOFA and SOFA Score (Sepsis)
  - CKD-EPI 2021
  - Anion Gap and Corrected Sodium
  - **And more!**
- **Normal lab reference values** organized by age and test type
- **Medical record creator** with export and editing
- **Local storage** with full offline access
- **Modern, fluid, and responsive interface**
- **Permanent dark mode**
- **Modular and expandable design**

## Technologies Used

- **Python 3.10+**
- **[Flet](https://flet.dev/)** – Web and desktop UI framework
- **Modular and scalable architecture**

## Installation and Execution

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Julian-Almario/medcore_app.git
    cd medcore_app/src
    ```
2. **Install dependencies:**
    ```bash
    pip install flet
    ```
3. **Run the app:**
    ```bash
    python main.py
    ```
> **Note:** Using a virtual environment is recommended.

## Project Structure

```text
app/
│
├── main.py                  # Entry point
├── README.md                # Main documentation
├── LICENSE                  # License
├── CODE_OF_CONDUCT.md       # Code of Conduct
├── pyproject.toml           # Flet configuration
├── app/
│   ├── modules/             # Modules and components
│   └── assets/              # Images and icons
│
├── storage/
│   └── data/
│       ├── historias_clinicas/
│       └── meds.json
```

## Current Status

* [x] Full offline access
* Normal lab reference values:

  * [x] Complete Blood Count (CBC)
  * [x] CSF analysis
  * [x] Urinalysis
* Most used medical calculators:

  * [x] Body Mass Index (BMI)
  * [x] Rule of Three (Direct)
  * [x] Mid-parental height
  * [x] GFR – Schwartz 2009 Equation
  * [x] SLICC Criteria for SLE Diagnosis
  * [x] qSOFA (Sepsis)
  * [x] SOFA Score (Sepsis)
  * [x] CKD-EPI 2021
  * [x] Anion Gap
  * [x] Corrected Sodium
* [x] Medications database
* [x] Interactive search
* [x] Medical record creator

## Objective

**MedCore** aims to be a reference tool for medical students, general practitioners, and specialists by centralizing calculations, normal values, and key parameters to speed up clinical decision-making.

## Frequently Asked Questions

**Can I use MedCore without an internet connection?**
Yes! All main features are available offline.

**How can I report a bug or suggest an improvement?**
Open an [issue here](https://github.com/Julian-Almario/medcore_app/issues).

## Contributions

Contributions are welcome! Check out the [contribution guide](CONTRIBUTING.md) or open a [pull request](https://github.com/Julian-Almario/medcore_app/pulls).

## License

This project is licensed under the **GNU GPL v3**. See the [`LICENSE`](LICENSE) file for more details.

## Acknowledgements

* Thanks to the Flet community and all contributors.
* Inspired by the need for accessible and modern medical tools.