"""
Neutron Mass Measurement — Calibration & Analysis
==================================================
We use the reaction  n + p -> d + gamma  to determine the neutron mass.
Since the proton and deuteron masses are known, measuring the gamma energy gives:

    m_n = m_d + m_gamma - m_p

Known masses:
    m_p = 938.272  MeV/c^2
    m_d = 1875.612 MeV/c^2

Workflow:
    1. Fit Gaussians to calibration source peaks to find channel positions
    2. Fit a linear calibration curve E(ch)
    3. Fit a Gaussian to the deuteron-gamma peak to find its channel
    4. Convert to energy and compute the neutron mass
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import linregress

import os
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/neutrons/"  # path to folder containing .txt data files

# Known physical constants (MeV/c^2)
M_PROTON   = 938.272
M_DEUTERON = 1875.612
M_NEUTRON_LIT = 939.565  # literature value for comparison


# =============================================================================
# Helper functions
# =============================================================================

def load_spectrum(filename):
    """Load a two-column (channel, counts) spectrum text file."""
    return np.loadtxt(DATA_DIR + filename, unpack=True)


def gaussian(x, a, b, c):
    """Standard Gaussian: a * exp(-(x-b)^2 / (2c^2))"""
    return a * np.exp(-(x - b)**2 / (2 * c**2))


def fit_gaussian_peak(channel, counts, ch_min, ch_max):
    """
    Fit a Gaussian to a peak in the range [ch_min, ch_max].

    Returns
    -------
    popt   : array [a, b, c]  — amplitude, center, width
    perr   : array            — 1-sigma uncertainties on popt
    x_peak : float            — channel of the peak maximum
    x_fit  : array            — channel values used in the fit
    y_fit  : array            — count values used in the fit
    """
    mask = (channel >= ch_min) & (channel <= ch_max)
    x_fit, y_fit = channel[mask], counts[mask]

    p0 = [np.max(y_fit), np.mean(x_fit), np.std(x_fit)]
    popt, pcov = curve_fit(gaussian, x_fit, y_fit, p0=p0)
    perr = np.sqrt(np.diag(pcov))

    x_model = np.linspace(ch_min, ch_max, 1000)
    x_peak  = x_model[np.argmax(gaussian(x_model, *popt))]

    return popt, perr, x_peak, x_fit, y_fit


def plot_gaussian_fit(channel, counts, popt, x_fit, y_fit,
                      x_peak, title, xlim, ylim=None):
    """Plot spectrum data with overlaid Gaussian fit and annotated parameters."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(channel, counts, 'b.', ms=4, label='Data')
    ax.plot(x_fit, gaussian(x_fit, *popt), 'r-', lw=2, label='Gaussian fit')
    ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    ax.set_xlabel('Channel')
    ax.set_ylabel('Counts')
    ax.set_title(title)

    textstr = (r'$f(x)=a\,e^{-(x-b)^2/2c^2}$' + '\n'
               f'$a={popt[0]:.2f}$\n'
               f'$b={popt[1]:.2f}$\n'
               f'$c={popt[2]:.2f}$\n'
               f'$x_{{peak}}={x_peak:.2f}$')
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.6))
    ax.legend()
    plt.tight_layout()
    plt.show()


# =============================================================================
# 1. Calibration — Gaussian fits to known sources
# =============================================================================
# Each source has known emission energies. We fit a Gaussian to each photopeak
# to find the corresponding channel number.
#
# Source  | Energy (keV)
# --------|-------------
# Na-22   | 511
# Co-60   | 1173.2
# Co-60   | 1332.5
# Cs-137  | 662

# --- Na-22 at 511 keV ---
ch_na, cts_na = load_spectrum("na24_calibration_500.txt")
popt_na, perr_na, xpeak_na, xf, yf = fit_gaussian_peak(ch_na, cts_na, 127, 165)
plot_gaussian_fit(ch_na, cts_na, popt_na, xf, yf,
                  xpeak_na, "Na-22 Calibration — 511 keV peak", xlim=(127, 165))
print(f"Na-22  (511.0 keV):   peak at channel {xpeak_na:.2f} ± {perr_na[1]:.2f}")

# --- Co-60 at 1173.2 keV ---
ch_co, cts_co = load_spectrum("Cobalt_calibration_500.txt")
popt_co1, perr_co1, xpeak_co1, xf, yf = fit_gaussian_peak(ch_co, cts_co, 300, 355)
plot_gaussian_fit(ch_co, cts_co, popt_co1, xf, yf,
                  xpeak_co1, "Co-60 Calibration — 1173.2 keV peak", xlim=(300, 355))
print(f"Co-60  (1173.2 keV):  peak at channel {xpeak_co1:.2f} ± {perr_co1[1]:.2f}")

# --- Co-60 at 1332.5 keV ---
popt_co2, perr_co2, xpeak_co2, xf, yf = fit_gaussian_peak(ch_co, cts_co, 355, 400)
plot_gaussian_fit(ch_co, cts_co, popt_co2, xf, yf,
                  xpeak_co2, "Co-60 Calibration — 1332.5 keV peak", xlim=(355, 400))
print(f"Co-60  (1332.5 keV):  peak at channel {xpeak_co2:.2f} ± {perr_co2[1]:.2f}")

# --- Cs-137 at 662 keV ---
ch_cs, cts_cs = load_spectrum("Cesium_calibration_500.txt")
popt_cs, perr_cs, xpeak_cs, xf, yf = fit_gaussian_peak(ch_cs, cts_cs, 170, 210)
plot_gaussian_fit(ch_cs, cts_cs, popt_cs, xf, yf,
                  xpeak_cs, "Cs-137 Calibration — 662 keV peak", xlim=(170, 210))
print(f"Cs-137 (662.0 keV):   peak at channel {xpeak_cs:.2f} ± {perr_cs[1]:.2f}")


# =============================================================================
# 2. Linear calibration fit — E(ch)
# =============================================================================
cal_channels = np.array([xpeak_na, xpeak_co1, xpeak_co2, xpeak_cs])
cal_energies = np.array([511.0, 1173.2, 1332.5, 662.0])

slope, intercept, r_value, p_value, std_err = linregress(cal_channels, cal_energies)

print(f"\nCalibration fit: E(ch) = {slope:.4f} * ch + {intercept:.4f}  [keV]")
print(f"R² = {r_value**2:.6f},  standard error on slope = {std_err:.4f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(cal_channels, cal_energies, zorder=5, label='Calibration points')
ch_range = np.linspace(cal_channels.min() - 10, cal_channels.max() + 10, 200)
ax.plot(ch_range, slope * ch_range + intercept, 'r-', label='Linear fit')
ax.set_xlabel('Channel')
ax.set_ylabel('Energy (keV)')
ax.set_title('Linear Fit for E(ch)')
ax.text(0.05, 0.85,
        f'Slope: {slope:.2f} keV/ch\nY-intercept: {intercept:.2f} keV',
        transform=ax.transAxes, fontsize=12,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.6))
ax.legend()
plt.tight_layout()
plt.show()


# =============================================================================
# 3. Deuteron-gamma peak — 2 lead, max paraffin, port open
# =============================================================================
# Fit a Gaussian to the peak around channel 600-650.
# This corresponds to gammas from  n + p -> d + gamma.

ch_sig, cts_sig = load_spectrum("2leadmaxparaffin_500.txt")
popt_sig, perr_sig, xpeak_sig, xf, yf = fit_gaussian_peak(ch_sig, cts_sig, 580, 650)
plot_gaussian_fit(ch_sig, cts_sig, popt_sig, xf, yf,
                  xpeak_sig,
                  "Gaussian Fit — Deuteron Gamma Peak (2 Lead, Max Paraffin)",
                  xlim=(580, 650), ylim=(0, 400))

ch_uncertainty = perr_sig[1]
print(f"\nDeuteron-gamma peak channel: {xpeak_sig:.2f} ± {ch_uncertainty:.2f}")


# =============================================================================
# 4. Neutron mass calculation
# =============================================================================
# Convert peak channel -> gamma energy [keV -> MeV], then apply:
#     m_n = m_d + m_gamma - m_p

E_gamma_keV  = slope * xpeak_sig + intercept
E_gamma_MeV  = E_gamma_keV / 1000.0
dE_gamma_MeV = slope * ch_uncertainty / 1000.0   # uncertainty propagation

m_neutron  = M_DEUTERON + E_gamma_MeV - M_PROTON
dm_neutron = dE_gamma_MeV

percent_error = abs(m_neutron - M_NEUTRON_LIT) / M_NEUTRON_LIT * 100

print("\n" + "=" * 45)
print(f"Peak channel:       {xpeak_sig:.2f} ± {ch_uncertainty:.2f}")
print(f"Gamma energy:       {E_gamma_MeV:.4f} ± {dE_gamma_MeV:.4f} MeV")
print(f"Neutron mass:       {m_neutron:.4f} ± {dm_neutron:.4f} MeV/c²")
print(f"Literature value:   {M_NEUTRON_LIT:.3f} MeV/c²")
print(f"Percent error:      {percent_error:.4f}%")
print("=" * 45)