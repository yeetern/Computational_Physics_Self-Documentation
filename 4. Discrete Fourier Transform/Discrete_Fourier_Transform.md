# DFT De-noising of a Noisy Sine Signal (SIF3012, Block 4)

**Course:** SIF3012 Computational Physics  
**Lecturer:** Juan Carlos Algaba  
**Problem type:** Signal processing + Fourier methods (DFT/IDFT)  

This block demonstrates **de-noising in the frequency domain** using the **Discrete Fourier Transform (DFT)** implemented **from definition** (no `np.fft`), then filtering and reconstructing the signal using the **Inverse DFT (IDFT)**.

The official problem statement is given in the course handout :contentReference[oaicite:0]{index=0}.

---

## 1. Problem Overview

We generate a clean signal
\[
f(t)=\sin(2\pi f_1 t)+\sin(2\pi f_2 t),
\]
with \( f_1 = 50\,\text{Hz} \) and \( f_2 = 120\,\text{Hz} \), sampled on \( t \in [0, 0.25) \) with \(\Delta t = 0.001\) s.

Then:
1. Add **white Gaussian noise** to create a noisy time series.
2. Compute the **DFT** and plot the **power spectrum** \(|F_k|^2\).
3. Apply an **ideal band-pass** filter around 50 Hz and 120 Hz.
4. Use **IDFT** to reconstruct a de-noised signal and compare (including RMS error).

---

## 2. What We Learn (Key Takeaways)

### (a) DFT connects time samples to frequency components
DFT definition:
\[
F_k = \sum_{n=0}^{N-1} f_n e^{-i2\pi kn/N}.
\]
IDFT definition:
\[
f_n=\frac{1}{N}\sum_{k=0}^{N-1}F_k e^{+i2\pi kn/N}.
\]

Interpretation:
- Each \(F_k\) is the "amount" of a sinusoid at frequency bin \(k\).
- Broadband noise spreads across many bins; real signal peaks cluster around true tones.

### (b) Sampling matters (Nyquist + frequency resolution)
With sampling frequency \( f_s = 1/\Delta t\):
- Nyquist limit: \( f_N = f_s/2 \)
- Frequency bin spacing: \(\Delta f = f_s/N\)

So whether peaks are “sharp” depends on:
- total duration \(T = N\Delta t\) (sets \(\Delta f\))
- whether tone frequencies align exactly with bins (spectral leakage)

### (c) Filtering is model-based
The “ideal band-pass” approach assumes:
- we know approximately where the real frequencies are,
- noise is broadband,
- the signal is sparse in frequency.

This is why the method is strong for **known-tone de-noising**.

---

## 3. Method Summary (Logic Chain)

1. Generate clean signal \(f(t)\).
2. Add noise: \(f_{\text{noisy}}(t)=f(t)+\epsilon(t)\).
3. Compute DFT: \(F_{\text{noisy}}(k)\).
4. Compute spectrum: \(\text{PSD}(k)\propto |F_{\text{noisy}}(k)|^2\).
5. Keep bins near 50 Hz and 120 Hz, zero-out the rest.
6. IDFT → reconstructed signal \(f_{\text{filtered}}(t)\).
7. Quantify improvement using RMS:
\[
\mathrm{RMS}=\sqrt{\langle (f_{\text{est}}-f_{\text{clean}})^2\rangle}.
\]

---

## 4. Numerical Limitations & Practical Notes

### (a) Manual DFT is expensive
The definition-based DFT costs:
- \(O(N^2)\) operations (double loop)

FFT costs:
- \(O(N\log N)\)

So manual DFT is excellent for learning, but not scalable.

### (b) Spectral leakage (finite window)
If the sampled window does not contain an integer number of cycles, power spreads into neighboring bins.
Practical fixes:
- window functions (Hann/Hamming),
- longer duration (smaller \(\Delta f\)),
- smarter peak-picking.

### (c) Filtering width trades off bias vs noise removal
- Too narrow: may remove real signal energy (distortion).
- Too wide: leaves too much noise.

---

## 5. Core Code (Reference Implementation)

This is the reusable “core” for future revision: **DFT, IDFT, frequency axis, and ideal band-pass**.

### (a) DFT / IDFT (definition)

```python
import numpy as np
import math

def dft(x):
    x = np.asarray(x, dtype=complex)
    N = x.size
    X = np.zeros(N, dtype=complex)

    for k in range(N):
        s = 0.0 + 0.0j
        for n in range(N):
            angle = -2.0 * math.pi * k * n / N
            s += x[n] * complex(math.cos(angle), math.sin(angle))
        X[k] = s
    return X

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
```

### (b) Frequency axis + PHD

```python
def frequency_axis(N, dt):
    fs = 1.0 / dt
    k = np.arange(N)
    freqs = k * fs / N
    return freqs, fs

def psd_from_dft(X, N):
    return (np.abs(X)**2) / (N**2)
```

### (c) Ideal band-pass filter around known tones

```python
def ideal_bandpass(X, freqs, fs, centers, width):
    X_filtered = np.zeros_like(X, dtype=complex)

    for f0 in centers:
        mask_pos = np.abs(freqs - f0) <= width
        mask_neg = np.abs(freqs - (fs - f0)) <= width  # negative-frequency partner
        mask = mask_pos | mask_neg
        X_filtered[mask] = X[mask]

    return X_filtered
```

### (d) Typical Usage Pattern

```python
# Given: noisy (time series), dt, and known tones f1, f2
N = len(noisy)
freqs, fs = frequency_axis(N, dt)

X_noisy = dft(noisy)
PSD = psd_from_dft(X_noisy, N)

X_filt = ideal_bandpass(X_noisy, freqs, fs, centers=[f1, f2], width=5.0)
filtered = idft(X_filt).real
```

---

## 6. How to Reuse This Code (Future Use)

You can reuse this framework for:

- **Any known-frequency signal**  
  (replace tone list / frequency centers)

- **Instrumental noise cleaning**  
  where the signal occupies narrow frequency bands

- **Peak detection + adaptive filtering**  
  (automate the choice of frequency centers)

- **Replacing manual DFT with FFT for speed**, using:
  - `np.fft.fft`
  - `np.fft.ifft`
  - `np.fft.fftfreq`

- **Extending to more advanced methods**, such as:
  - windowed FFT (STFT) for time-varying signals,
  - spectral estimation methods (Welch / multitaper),
  - imaging Fourier relations  
    (radio interferometry: *uv* plane ↔ image plane).

---

## 7. Instructor Feedback & Radio Astronomy Context

In radio astronomy, the **image** and the **visibility data** are a **Fourier transform pair**.

In practice, we do not only use FFT, but also algorithms such as:
- **CLEAN** (deconvolution),
- **self-calibration** (iterative correction for noise and calibration errors).

Weighting and gridding schemes are applied to:
- handle data availability,
- control noise and RMS trade-offs,
- emphasize compact versus extended structure.

### Workshop resources shared by the lecturer  
*(Harvard–Smithsonian / Synthesis Imaging)*

- **Slides (Imaging & Deconvolution Workshop PDF):**  
  https://science.nrao.edu/science/meetings/2014/14th-synthesis-imaging-workshop/lectures-files/wilner_siw2014.pdf

- **Recording / presentation:**  
  https://www.youtube.com/watch?v=mRUZ9eckHZg

### Interpretation (What this means for this assignment)

- The DFT filtering implemented here is a **toy version of a real imaging pipeline idea**:  
>isolate structure in Fourier space, then reconstruct in the image/time domain.

- CLEAN and self-calibration go beyond simple “band-pass” filtering by using:
  - physical priors (sparsity / regions),
  - iterative correction,
  - weighting choices in Fourier space.

---

## 8. Summary

Block 4 shows that:

- Fourier transforms reveal hidden structure under noise,
- filtering in frequency space can strongly reduce broadband noise,
- sampling settings control what frequencies can be resolved,
- manual DFT builds intuition, while FFT is essential for large-scale applications.
