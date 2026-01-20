#Assignment 4 Block 4
#Program Name: DFT De-noising of a Noisy Sine Signal
#Subject: SIF3012 Computational Physics
#Author: Tan Yee Tern
#Student ID: 23006131
#Email: 23006131@siswa.um.edu.my
#Date of Creation: Friday November 21

#Description:
#This program demonstrates de-noising using the Discrete Fourier Transform (DFT),
#implemented manually without calling any FFT library routine (i.e np.fft).
#We consider a signal:
#           f(t) = sin(2π f1 t) + sin(2π f2 t)
#with f1 = 50 Hz and f2 = 120 Hz, sampled from t = 0 to t = 0.25s with
#time step Δt = 0.001s. White Gaussian noise is added to obtain a noisy signal.
#Exercise 1:
#Generate the clean and noisy signals and plot them in the time domain.
#Exercise 2:
#Implement the DFT and inverse DFT (IDFT) manually using the definitions:
#       F_k = Σ_{n=0}^{N-1} f_n * exp(-i 2π k n / N)
#       f_n = (1/N) Σ_{k=0}^{N-1} F_k * exp(+i 2π k n / N)
#Use the DFT of the noisy signal to plot the power spectrum (|F_k|^2) vs frequency.
#Exercise 3:
#Filter the spectrum by keeping only the components near 50 Hz and 120 Hz,
#set all other frequency components to zero, then apply the IDFT to recover
#a de-noised signal. Plot and compare the clean, noisy and filtered signals.

#Comment:
#Dear Dr. Juan, in this block I avoided np.fft and code the DFT/IDFT directly
#from the definition. The aim is to see clearly how each frequency component is
#constructed from the time samples and how simple frequency-domain filtering
#can remove broadband noise.

#------------------------------------------------------------------------------
# Exercise 1

import numpy as np
import matplotlib.pyplot as plt
import math

# Define parameters

# Signal parameters as given
f1 = 50.0
f2 = 120.0
dt = 0.001         # time step(s)
t_i = 0            # initial time(s)
t_f = 0.25         # final time(s)

# Time grid
t = np.arange(t_i, t_f, dt)     # 0, 0.001, ..., 0.249
N = len(t)                      # number of samples
fs = 1.0 / dt                   # sampling frequency(Hz)
nyquist = fs / 2.0              # Nyquist frequency(Hz)

# Noise level
noise_sigma = 2.0           # standard deviation for Gaussian noise
np.random.seed(0)           # fixed seed for reproducibility
#Can try to change sigma value, if small might be invisible
#If large, noise might dominant and fail to be filtered

# Clean and noisy signals
# Clean: f(t) = sin(2π f1 t) + sin(2π f2 t)
clean = np.sin(2.0 * math.pi * f1 * t) + np.sin(2.0 * math.pi * f2 * t)
# White Gaussian noise
noise = noise_sigma * np.random.randn(N)
# Noisy signal = clean signal + white Gaussian noise
noisy = clean + noise

# For confirmation of Sampling settings
print("Exercise 1:")
print(f"Number of samples N = {N}, sampling frequency fs = {fs:.1f} Hz")
print("Clean and noisy signals are generated.\n")

# Plot the graph
plt.figure(figsize=(8, 4))
plt.plot(t, clean, 'black', linewidth=2.0, label="Clean")
plt.plot(t, noisy, 'red', linewidth=1.0, alpha=0.7, label="Noisy")
plt.xlabel("Time, s")
# Adjust linewidth and alpha to standout Clean signal
plt.ylabel("f(t)")
plt.title("Exercise 1: Clean vs Noisy Signal")
plt.grid(True, linestyle='--', alpha=0.5) #add grid with transparency
plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------------------
# Exercise 2

# Define Discrete Fourier Transform(DFT) function
# Input = x : array of length N (time-domain samples)
# Output = X : array of length N (frequency-domain coefficients)
# Definition:
#    X[k] = Σ_{n=0}^{N-1} x[n] * exp(-i 2π k n / N)
def dft(x):
    x = np.asarray(x, dtype=complex) #Array of Complex Number
    N = x.size
    X = np.zeros(N, dtype=complex)

    # Double loop: O(N^2)
    for k in range(N):
        s = 0.0 + 0.0j
        for n in range(N):
            angle = -2.0 * math.pi * k * n / N
            s += x[n] * complex(math.cos(angle), math.sin(angle))
            # exp(-i angle) = cos (angle) + i sin (angle)
        X[k] = s
    return X

# Define Inverse Discrete Fourier Transform(IDFT) function
# Input = X : array of length N (frequency-domain coefficients)
# Output = x : array of length N (time-domain samples)
# Definition:
#     x[n] = (1/N) Σ_{k=0}^{N-1} X[k] * exp(+i 2π k n / N)
def idft(X):
    X = np.asarray(X, dtype=complex)
    N = X.size
    x = np.zeros(N, dtype=complex)

    for n in range(N):
        s = 0.0 + 0.0j
        for k in range(N):
            angle = 2.0 * math.pi * k * n / N
            s += X[k] * complex(math.cos(angle), math.sin(angle))
        x[n] = s / N
    return x

X_noisy = dft(noisy)

# Frequency array for plotting (corresponding to k indices)
k = np.arange(N)
freqs = k * fs / N  # 0, fs/N, 2fs/N, ...

# Power spectral density
PSD = (np.abs(X_noisy)**2) / N**2

# Plot only up to Nyquist frequency (first N//2 points) where // means integer division
half = N // 2

plt.figure(figsize=(8, 4))
plt.plot(freqs[:half], PSD[:half], 'r', linewidth=1.0, label="Noisy")
plt.xlabel("Frequency, Hz")
plt.ylabel("PSD (Normalized)")
plt.title("Exercise 2: Power Spectrum of Noisy Signal")
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(0, 500)  # Nyquist is 500 Hz for fs = 1000 Hz
plt.legend()
plt.tight_layout()
plt.show()

print("Exercise 2:")
print("PSD vs Frequency graph is plotted.\n")

#------------------------------------------------------------------------------
# Exercise 3

print("Exercise 3:")
print("Filter spectrum to keep only components near 50 Hz and 120 Hz.\n")

# Define Filter function (keep certain frequency)

#Parameters:
#    X       : DFT coefficients (length N)
#    freqs   : frequency array for bins k
#    fs      : sampling frequency
#    centers : list of central frequencies to keep (e.g. [50, 120])
#    width   : half-width of band around each center (Hz)
#Output:
#    X_filtered : filtered spectrum with unwanted components set to zero

def ideal_bandpass(X, freqs, fs, centers, width):
    X_filtered = np.zeros_like(X, dtype=complex)
    N = len(X)

    for f0 in centers:
        # Using Boolean Masking rather than if loop, more simple
        # Positive-frequency bin
        mask_pos = np.abs(freqs - f0) <= width

        # Negative-frequency partner appears at fs - f0 in the DFT indexing
        mask_neg = np.abs(freqs - (fs - f0)) <= width
        # Negative partner for f0 = 50 Hz, with fs = 1000 Hz is 950 Hz

        mask = mask_pos | mask_neg
        X_filtered[mask] = X[mask]

    return X_filtered

# Choose bands around 50 Hz and 120 Hz (±5 Hz for example)
centers = [f1, f2]
band_halfwidth = 5.0 #+/- around centers

X_filtered = ideal_bandpass(X_noisy, freqs, fs, centers, band_halfwidth)

# IDFT to recover filtered time-domain signal
filtered_complex = idft(X_filtered)
filtered = filtered_complex.real   # original signal is real

# Plot power spectrum of filtered vs original noisy
PSD_filtered = (np.abs(X_filtered)**2) / N**2

plt.figure(figsize=(8, 4))
plt.plot(freqs[:half], PSD[:half], 'red', linewidth=1.0, alpha=0.6, label="Noisy")
plt.plot(freqs[:half], PSD_filtered[:half], 'blue', linewidth=1.5, label="Filtered")
plt.xlabel("Frequency, Hz")
plt.ylabel("PSD (Normalized)")
plt.title("Exercise 3: PSD for Noisy vs Filtered")
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(0, 500)
plt.legend()
plt.tight_layout()
plt.show()

# Time-domain comparison: clean vs noisy vs filtered
plt.figure(figsize=(8, 4))
plt.plot(t, clean, 'black', linewidth=1.5, alpha=0.8, label="Clean")
plt.plot(t, noisy, 'red', linewidth=0.8, alpha=0.4, label="Noisy")
plt.plot(t, filtered, 'blue', linewidth=2, label="Filtered")
plt.xlabel("Time, s")
plt.ylabel("f(t)")
plt.title("Exercise 3: De-noised Signal")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# Comparison
rms_noisy   = np.sqrt(np.mean((noisy - clean)**2))
rms_filtered = np.sqrt(np.mean((filtered - clean)**2))

print("Signal diagram is plotted.\n")
print(f"RMS error noisy = {rms_noisy:.3f}, filtered = {rms_filtered:.3f}\n")
print("Program finished.")
#End of program

#Conclusion:
#By implementing the DFT and IDFT from their definitions and applying an
#ideal band-pass around 50 Hz and 120 Hz, we successfully removed most of the
#broadband Gaussian noise. In the frequency domain, the filtered spectrum
#retains only the two dominant peaks and in the time domain the reconstructed
#signal closely matches the original clean waveform, with a much smaller RMS
#error than the noisy signal. This demonstrates how Fourier methods can be used
#for de-noising when the relevant frequency content of the signal is known.

#------------------------------------------------------------------------------
# Alternative way: using np.fft

"""
print("FFT version:")
X_noisy = np.fft.fft(noisy)
freqs = np.fft.fftfreq(N, d=dt)
PSD = np.abs(X_noisy)**2 / N**2
half = N // 2

plt.figure(figsize=(8, 4))
plt.plot(freqs[:half], PSD[:half], label="Noisy")
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD (normalized)")
plt.title("FFT version: Power Spectrum of Noisy Signal")
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(0, 500)
plt.legend()
plt.tight_layout()
plt.show()

centers = [f1, f2]
band_halfwidth = 5.0

X_filtered = np.zeros_like(X_noisy, dtype=complex)

for f0 in centers:
    mask = (np.abs(freqs - f0) <= band_halfwidth) | \
           (np.abs(freqs + f0) <= band_halfwidth)
    X_filtered[mask] = X_noisy[mask]

PSD_filt = np.abs(X_filtered)**2 / N**2

plt.figure(figsize=(8, 4))
plt.plot(freqs[:half], PSD[:half],  label="Noisy", alpha=0.5)
plt.plot(freqs[:half], PSD_filt[:half], label="Filtered", linewidth=2)
plt.xlabel("Frequency, Hz")
plt.ylabel("PSD (normalized)")
plt.title("FFT version: PSD of Noisy vs Filtered")
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(0, 500)
plt.legend()
plt.tight_layout()
plt.show()

filtered = np.fft.ifft(X_filtered).real

rms_noisy = np.sqrt(np.mean((noisy - clean)**2))
rms_filt  = np.sqrt(np.mean((filtered - clean)**2))

print(f"RMS error (noisy  - clean)    = {rms_noisy:.3f}")
print(f"RMS error (filtered - clean) = {rms_filt:.3f}\n")

plt.figure(figsize=(8, 4))
plt.plot(t, clean,   'k',  linewidth=1.5, alpha=0.8, label="Clean")
plt.plot(t, noisy,   'r',  linewidth=0.8, alpha=0.4, label="Noisy")
plt.plot(t, filtered,'b',  linewidth=2.0, alpha=0.9, label="Filtered (FFT)")
plt.xlabel("Time [s]")
plt.ylabel("f(t)")
plt.title("FFT version: De-noised Signal via np.fft")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

print("FFT-based program finished.")
"""

#Conclusion:
#In contrast, np.fft performs the same transform using the Cooley–Tukey FFT
#algorithm, which reduces the computational cost to O(N log N). Implementing
#FFT manually is significantly more involved, because it requires:
#1. bit-reversal permutations
#2. recursive butterfly structures
#3. the Cooley–Tukey decomposition of the DFT.
#These elements make FFT implementation non-trivial for students, but these also
#explain why scientific codes rely on optimized libraries (NumPy, FFTW, MKL)
#instead of re-writing FFT by hand.

#Further Questions:
#Working through the manual DFT clarified the mathematical structure of the
#transform, but it also raises several questions I would like to explore:
#1. In practical radio-astronomy pipelines (AIPS, CASA, DIFMAP), how are FFT-
#   based methods optimized for large data sets? For example, what strategies
#   are used to handle very noisy data and large numbers of samples?

#2. Beyond simple band-pass filtering, what more advanced frequency-domain
#   de-noising techniques (e.g. CLEAN, multi-taper methods, wavelets) are
#   commonly used when noise overlaps with the signal band, making filtering
#   more difficult?

#3. For imaging problems, how does the FFT interact with the convolution
#   theorem, gridding and uv-plane sampling? I would like to understand how
#   these ideas connect to interferometry and radio maps.

#4. As I try to understand which direction I might take for my future FYP,
#   I would like to learn more about possible computational or radio-astronomy
#   applications. I am not yet familiar with the full workflow (e.g., AGN
#   variability studies, FRB signal processing, imaging pipelines), so I would
#   appreciate suggestions on small exploratory projects or topics that could
#   help me understand these areas better before deciding on a direction.

# Best regards,
# Tan Yee Tern

#Reference: https://numpy.org/doc/stable/reference/routines.fft.html