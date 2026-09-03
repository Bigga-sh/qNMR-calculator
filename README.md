# qNMR Calculator

A desktop application for **quantitative NMR (qNMR) analysis** of reaction mixtures.  
Enter your internal standard, starting material, products and byproducts with their NMR integrals and the app computes **moles, conversion, yield and selectivity** in one click.

---

## Features

- **Reaction analysis** — conversion, molar yield and selectivity for any number of products and byproducts
- **Purity determination** — dedicated purity-check dialog (n_analyte / m_sample × MW)
- **Structure drawing** — integrated JSME molecular editor; draw a structure and MW is filled automatically (requires RDKit)
- **Mass ↔ mmol sync** — changing mass auto-updates mmol and vice versa
- **Session save / load** — save your experiment as a JSON file and reload it later
- **Excel export** — one-click export of results to a formatted `.xlsx` file

---

## Method

The calculation follows the **IUPAC qNMR formula**:

```
n_X = n_IS × (A_X / A_IS) × (N_IS / N_X)
```

where:
- `n_IS` = moles of internal standard = mass_IS / MW_IS  
- `A_X`, `A_IS` = integrated NMR signal areas of compound X and the internal standard  
- `N_IS`, `N_X` = number of equivalent protons in the integrated signal

Derived quantities:
```
Conversion (%)    = (1 − n_SM_remaining / n_SM_initial) × 100
Yield_X (%)       = (n_X / n_SM_initial) × 100
Selectivity_X (%) = (n_X / Σ n_products+byproducts) × 100
```

---

## Requirements

- Python 3.10 or newer
- Windows / macOS / Linux

---

## Installation

```bash
pip install -r requirements.txt
```

> **Note for conda users:** if `pip install rdkit` fails, use `conda install -c conda-forge rdkit` instead.  
> The app works without RDKit — structure previews and MW auto-fill will simply be unavailable.

---

## Running the app

**Windows** — double-click `Launch App.bat`

**Any platform** — run from a terminal:

```bash
python qNMR_gui.py
```

---

## How to use

### Reaction analysis (main window)

1. **Internal Standard** panel — fill in name, draw the structure (MW auto-fills), enter the weighed mass and the NMR integral area. Set *N* to the number of equivalent protons in the integrated signal.
2. **Starting Material** panel — fill in the compound, its initial weighed mass, and the NMR area of the remaining SM (set to 0 if fully consumed).
3. Click **+ Add Product** / **+ Add Byproduct** for each compound observed. Fill in MW, N and area.
4. Click **Calculate** — the results table shows moles, mass, yield and selectivity; the summary bar shows conversion.
5. Use **Export Excel** to save the table, or **Save session** to preserve all inputs as a JSON file.

### Purity check

Click **Purity Check** (toolbar or Tools menu):
1. Fill in the **Internal Standard** (same as above).
2. Fill in the **Analyte** — enter the total weighed mass of the sample in *Sample mass* (this may contain impurities).
3. Click **Calculate Purity**.

```
Purity (%) = (n_analyte × MW_analyte) / m_sample × 100
```

---

## Project structure

```
qNMR calculator/
├── qNMR_gui.py          # PyQt6 GUI (main entry point)
├── qNMR.py              # Core calculation logic (dataclasses + QNMRCalculator)
├── resources/
│   ├── editor.html      # JSME structure editor host page
│   └── jsme/            # JSME library files (MIT licensed)
├── qNMRicon.ico         # Application icon
├── qNMR.spec            # PyInstaller spec — only needed to build a standalone .exe
├── pyi_rth_webengine.py # PyInstaller runtime hook for Qt WebEngine
├── requirements.txt
└── Launch App.bat       # Windows one-click launcher
```

---

## Building a standalone executable (optional)

If you want to distribute a `.exe` that does not require Python to be installed:

```bash
pip install pyinstaller
pyinstaller qNMR.spec
```

The compiled app will be in `dist/qNMR_Calculator/`.

> **Note:** the `.spec` file contains absolute paths set for the original author's machine.  
> Before running PyInstaller, open `qNMR.spec` and update the `pathex` and `_conda_lib` variables to match your own paths.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Structure editor shows blank / fails to load | Ensure `resources/editor.html` and `resources/jsme/` are present next to `qNMR_gui.py` |
| No structure preview / MW not auto-filled | Install RDKit: `pip install rdkit` or `conda install -c conda-forge rdkit` |
| `ModuleNotFoundError: PyQt6.QtWebEngineWidgets` | Run `pip install PyQt6-WebEngine` |
| App crashes on macOS with OpenGL error | Try running with `QT_OPENGL=desktop python qNMR_gui.py` |
