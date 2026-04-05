"""
Neutron Mass Measurement — Spectra Plots
=========================================
Raw NaI+PMT detector spectra for each experimental configuration of the neutron howitzer.
Each trial was run for 500s. The x-axis is detector channel; the y-axis is counts.

Configurations explored:
  - No shielding (port open and closed)
  - Lead only (3 pieces, ~4.7-4.8 cm each)
  - Graphite only vs. paraffin only (no lead)
  - Lead + graphite vs. lead + paraffin (port open)
  - Lead before vs. after paraffin (order test)
  - Calibration sources (Na-22, Co-60, Cs-137)
"""

import numpy as np
import matplotlib.pyplot as plt

import os
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/neutrons/"  # path to folder containing .txt data files


def load_spectrum(filename):
    """Load a two-column (channel, counts) spectrum text file."""
    return np.loadtxt(DATA_DIR + filename, unpack=True)


def plot_spectrum(filename, title, xlim=None, ylim=None, save_as=None):
    """Load and plot a single spectrum."""
    channel, counts = load_spectrum(filename)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(channel, counts)
    ax.set_xlabel("Channel")
    ax.set_ylabel("Counts")
    ax.set_title(title)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    plt.tight_layout()
    if save_as:
        fig.savefig(save_as, dpi=300)
    plt.show()


def plot_spectra_pair(file1, title1, file2, title2, xlim=None):
    """Plot two spectra side by side for easy comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    for ax, fname, title in zip(axes, [file1, file2], [title1, title2]):
        ch, counts = load_spectrum(fname)
        ax.plot(ch, counts)
        ax.set_xlabel("Channel")
        ax.set_ylabel("Counts")
        ax.set_title(title)
        if xlim:
            ax.set_xlim(xlim)
    plt.tight_layout()
    plt.show()


# -----------------------------------------------------------------------------
# 1. No shielding between howitzer and detector
# -----------------------------------------------------------------------------
plot_spectra_pair(
    "0lead_closed_500.txt", "0 Lead, Port Closed",
    "0lead_open_500.txt",   "0 Lead, Port Open"
)

# -----------------------------------------------------------------------------
# 2. Lead only (3 pieces, port closed and open)
#    Demonstrates that lead effectively attenuates gammas from the howitzer.
# -----------------------------------------------------------------------------
plot_spectra_pair(
    "3lead_closed_500.txt",       "3 Lead, Port Closed",
    "3lead_nothing_open_500.txt", "3 Lead, Port Open"
)

# -----------------------------------------------------------------------------
# 3. Graphite vs. paraffin only (no lead, port closed)
#    Graphite (pure carbon) is the control — deuteron formation with carbon is unlikely.
#    The slightly higher peak ~ch750 with paraffin indicates n+p collisions.
# -----------------------------------------------------------------------------
plot_spectra_pair(
    "0lead_maxgraphite_closed_500.txt", "0 Lead, Max Graphite, Port Closed",
    "0lead_maxparaffin_closed_500.txt", "0 Lead, Max Paraffin, Port Closed"
)

# -----------------------------------------------------------------------------
# 4. Lead + graphite vs. lead + paraffin (port open)
#    With lead blocking howitzer gammas, the residual peak in the paraffin case
#    comes from deuteron-formation gammas.
# -----------------------------------------------------------------------------
plot_spectra_pair(
    "3lead_maxgraphite_open_500.txt", "3 Lead, Max Graphite, Port Open",
    "3lead_maxparaffin_open500.txt",  "3 Lead, Max Paraffin, Port Open"
)

# -----------------------------------------------------------------------------
# 5. Max paraffin vs. min paraffin (lead before, port open)
#    More paraffin -> more n+p collision probability -> higher gamma peak.
# -----------------------------------------------------------------------------
plot_spectra_pair(
    "3lead_maxparaffin_open500.txt",  "3 Lead, Max Paraffin (~30 cm), Port Open",
    "3lead_minparaffin_open_500.txt", "3 Lead, Min Paraffin (~3.8 cm), Port Open"
)

# -----------------------------------------------------------------------------
# 6. Lead before vs. lead after paraffin
#    Lead placed *after* paraffin attenuates the signal gammas we want to detect.
# -----------------------------------------------------------------------------
plot_spectra_pair(
    "3lead_maxparaffin_open500.txt",  "Lead BEFORE Paraffin (correct order)",
    "maxparaffin_3lead_open_500.txt", "Lead AFTER Paraffin (attenuates signal)"
)

# -----------------------------------------------------------------------------
# 7. Calibration source spectra
#    Raw spectra for Na-22, Co-60, and Cs-137 used to calibrate channel -> energy.
# -----------------------------------------------------------------------------
calibration_sources = [
    ("3lead_sodium_closed_500.txt", "Na-22 Calibration (511 keV, 1.274 MeV)"),
    ("3lead_cobalt_closed_500.txt", "Co-60 Calibration (1.173 MeV, 1.332 MeV)"),
    ("3lead_cesium_closed_500.txt", "Cs-137 Calibration (662 keV)"),
]

for fname, title in calibration_sources:
    plot_spectrum(fname, title)