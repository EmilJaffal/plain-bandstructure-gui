# Plain Bandstructure GUI Plotter

## Overview

The **Plain Bandstructure GUI Plotter** is a Python-based web application for interactive visualization of electronic band structures from VASP calculations. Built with [Dash](https://dash.plotly.com/) and [PyProcar](https://github.com/romerogroup/pyprocar), it allows users to quickly plot band structures from standard VASP output files, customize graph settings (including Fermi energy), and export high-quality PNG images.

---

## Features

- ✅ **Paste or input the path** to a folder containing `PROCAR`, `OUTCAR`, and `KPOINTS` (no zipping needed).
- ✅ **Interactive plotting** of the band structure using PyProcar.
- ✅ **Adjust Fermi energy** interactively.
- ✅ **Custom X/Y axis ranges** and axis/label toggles.
- ✅ **Live title & axis label toggles**.
- ✅ **High-quality PNG export** with folder-based filenames.
- ✅ **Error and warning messages** for missing or problematic files.
- ✅ **Demo data** included (`CeCoAl4` folder).

---

## Requirements

- Python ≥ 3.10
- [PyProcar v6.5.0](https://github.com/romerogroup/pyprocar/releases/tag/v6.5.0)
- `conda` environment recommended
- See `requirements.txt` for all dependencies.

---

## Directory Structure

Example directory tree (after cloning):

```
plain-bandstructure-gui/
├── app.py
├── requirements.txt
├── CeCoAl4/
│   ├── PROCAR
│   ├── OUTCAR
│   └── KPOINTS
├── ...
```

**You can use your own folder (e.g., `Y7Ru4InGe12/`) with the same file structure.**

---

## How It Works

1. **Input the path** to a folder containing `PROCAR`, `OUTCAR`, and `KPOINTS`.
2. **Adjust Fermi energy** and graph settings as needed.
3. **View the band structure plot** interactively in your browser.
4. **Download the plot** as a PNG file named after your folder (e.g., `Y7Ru4InGe12_bandstructure.png`).

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/emiljaffal/plain-bandstructure-gui
cd plain-bandstructure-gui
```

### 2. Install Dependencies

```bash
conda install --file requirements.txt
```
or
```bash
pip install -r requirements.txt
```

### 3. Launch App

```bash
python app.py
```

### 4. Access in Browser

Go to [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## Output

- One interactive band structure plot.
- Downloadable high-resolution PNG (`<folder>_bandstructure.png`).

---

## Demo Data

A demo folder `CeCoAl4` with example VASP outputs is included for testing.

---

## Notes

- **No ZIP upload needed:** Just use a folder with the required files.
- **PyProcar** is used for all band structure parsing and plotting ([PyProcar GitHub](https://github.com/romerogroup/pyprocar)).
- For issues or feature requests, open an issue on GitHub.

---

## License

MIT License. See LICENSE for details.

---

## Contact

For questions or collaborations, open an issue or contact via GitHub:

👉 [EmilJaffal/plain-bandstructure-gui](https://github.com/emiljaffal/plain-bandstructure-gui)

---