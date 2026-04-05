# Neutron Mass Measurement

Experimental determination of the neutron mass using a neutron howitzer and NaI+PMT gamma detector.

## Result

$$m_n = 939.51 \pm 0.78 \text{ MeV/c}^2$$

Literature value: **939.565 MeV/c²** (percent error: 0.006%)

## Method

We exploit the deuteron formation reaction:

$$n + p \rightarrow d + \gamma$$

Since the proton and deuteron masses are precisely known from mass spectroscopy, measuring the gamma energy gives us the neutron mass:

$$m_n = m_d + m_\gamma - m_p$$

A **neutron howitzer** (²³⁹Pu + ⁹Be source) provides energetic neutrons. Paraffin (CH₂) serves as the proton target. Lead shielding attenuates background gammas from the howitzer. An NaI+PMT detector records the gamma spectrum, calibrated with ²²Na, ⁶⁰Co, and ¹³⁷Cs sources.

## Repository Structure

```
neutron-mass-measurement/
├── README.md
├── data/                  # Raw .txt spectrum files (channel vs. counts, 500s runs)
├── 01_spectra_plots.py    # Exploratory spectra for all configurations
├── 02_analysis.py         # Calibration, Gaussian fits, and final calculation
└── report/
    └── Neutrons_Lab_Report.pdf
```

## Requirements

```
numpy
scipy
matplotlib
```

Install with:
```bash
pip install numpy scipy matplotlib
```

## How to Run

Run each script directly with Python:

```bash
python 01_spectra_plots.py
python 02_analysis.py
```

Or open them in PyCharm and click the green **Run** button.

Each plot opens in a popup window — close it to advance to the next one.

Make sure your `.txt` data files are in a `data/` subfolder next to the scripts, and that `DATA_DIR` at the top of each file points to it.

## Data Files

Each `.txt` file contains two whitespace-separated columns: `channel` and `counts`. Filenames encode the experimental configuration, e.g.:

- `3lead_maxparaffin_open500.txt` → 3 pieces of lead, maximum paraffin, port open, 500s run
- `Cesium_calibration_500.txt` → Cs-137 calibration source, 500s run

## Author

Talia Friedman — April 2023
