# DOSCAR GUI Plotter

## Purpose

The **DOSCAR GUI Plotter** is a Python-based web application designed to visualize Density of States (DOS) data from VASP calculations. It supports both spin-polarized (ISPIN=2) and non-spin-polarized (ISPIN=1) calculations, as well as various orbital projection schemes (LORBIT settings). The application provides an intuitive interface for uploading data, customizing plots, and exporting high-quality PNG visualizations.

---

## Features

- **Spin-Polarized and Non-Spin-Polarized Support**:
  - Handles ISPIN=1 (non-spin-polarized) and ISPIN=2 (spin-polarized) calculations.
  
- **Orbital Projection Support**:
  - Supports LORBIT settings:
    - **LORBIT=11-14**: Individual orbitals are resolved (e.g., px, py, pz, etc.).
    - **LORBIT=0, 1, 2, 5, 10**: Orbitals are grouped (e.g., total p-orbital contributions).

- **Customizable Graphs**:
  - Total DOS is plotted as the sum of atomic contributions, similar to wxDragon.
  - The total DOS is **not** plotted as in the first block (column 2) of the DOSCAR file because VASP projects a finite set of PAW spheres, excluding interstitial or delocalized sites.

- **Legend Sorting**:
  - The legend is sorted by **Mendeleev numbers** for intuitive ordering of elements.

- **Input Requirements**:
  - The uploaded ZIP file must contain a folder with the following:
    - **POSCAR**: Contains structural information.
    - **DOSCAR**: Contains DOS data.
  - The folder being zipped must be named after the molecule/compound title (e.g., `Gd10RuCd3`), as the graph title is derived from the folder name.
  - The ZIP file itself can have any name.

---

## Hosting

This application is hosted on **Heroku** and can be accessed at the following link:

[https://doscar-gui-9a48cc5d4e0d.herokuapp.com](here!)

Replace `your-heroku-app-name` with the actual name of your Heroku app.

---

## How It Works

### Parsing the DOSCAR File

- **First Block**:
  - The first block contains the total DOS and integrated DOS (IDOS). However, the total DOS is recalculated as the sum of atomic contributions to account for interstitial or delocalized sites.

- **Atomic Blocks**:
  - Each atomic block is parsed to extract orbital contributions. The number of columns in the atomic blocks determines the orbital resolution:
    - **4 Columns**: Grouped atomic contributions (e.g., s, p, d).
    - **7 Columns**: Spin-polarized grouped contributions (e.g., s↑, s↓, p↑, p↓, etc.).
    - **10 Columns**: Individual orbitals resolved (e.g., px, py, pz, etc.).
    - **19 Columns**: Spin-polarized individual orbitals resolved (e.g., px↑, px↓, py↑, py↓, etc.).

### Legend Sorting

- The legend is sorted by **Mendeleev numbers**, ensuring that elements are displayed in a chemically intuitive order.

---

## Future Updates

- **Plotting IDOS**:
  - Add support for plotting integrated DOS (IDOS) and spin-resolved IDOS.

- **Individual Atom Contributions**:
  - Enable plotting of individual atoms and their respective orbitals (e.g., Ge1, Ge2).

- **Dynamic Buffer for xmax**:
  - Adjust the buffer maximum dynamically based on the highest value within the selected energy window.

- **Option to Remove Total DOS**:
  - Provide an option to exclude the total DOS from the plot.

- **Fix Orbital Labeling with LaTeX**:
  - Improve orbital labels (e.g., `pₓ`, `pᵧ`, `p_z`) to use proper LaTeX formatting for better readability.

- **Legend Sorting Option**:
  - Add an option to customize legend sorting (e.g., by Mendeleev numbers, alphabetical order, or user-defined order).

---

## Usage Instructions

### How to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/doscar-gui.git
   cd doscar-gui
   ```

2. **Install Dependencies**:
   - Ensure you have Python 3.9 or later installed.
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   - Start the application:
     ```bash
     python app.py
     ```

4. **Access the Application**:
   - Open your browser and navigate to:
     ```
     http://127.0.0.1:8050/
     ```

5. **Upload Data**:
   - Upload a ZIP file containing a folder with `POSCAR` and `DOSCAR` files.
   - Ensure the folder name matches the molecule/compound title.

6. **Customize and Export**:
   - Adjust axis limits, legend position, and other settings.
   - Save the plot as a high-resolution PNG file.

---

## Example

### Input Folder Structure

```
Gd10RuCd3/
├── POSCAR
├── DOSCAR
```

### Output

- A PNG file of the DOS plot, similar to matplotlib, titled `Gd₁₀RuCd₃ DOS`.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or bug reports.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
