# 🖼️ 2D FFT Image Denoising – Periodic Noise Removal

## 📌 Problem Statement (What the Question Asks)

This task is part of **SIF3012 – Computational Physics (Continuous Assessment)**.

The question asks us to:

- Load a **corrupted image** (`AlternativeAssessment.png`)
- Remove **periodic undesired noise patterns** using **2D FFT**
- Reconstruct a **denoised image** using **inverse FFT**
- **Do not remove the central (brightest) FFT component**, since it represents the **average image intensity (DC term)**

In short:

> Use **2D FFT filtering** to suppress periodic noise while preserving the true image structure and brightness.

---

## 🧠 Physical & Numerical Idea

A periodic grid pattern in real space corresponds to **discrete peaks in Fourier space**.

- **True image content** → concentrated around **low frequencies** (near the center)
- **Periodic noise** → shows up as **strong symmetric peaks** away from the center

So the strategy is:

1. Transform the image into frequency space (FFT)
2. Detect unusually strong off-center peaks (noise)
3. Suppress them using a mask
4. Inverse FFT to recover the denoised image

---

## 🛠️ Approach (What I Did)

1. Load the image and convert to grayscale (if needed)
2. Compute the **2D FFT** and shift it so the DC component is at the center
3. Compute the **log-magnitude spectrum** for clearer peak visibility
4. Build a frequency mask that:
   - removes strong peaks (likely noise)
   - preserves the center region (protect DC / low-frequency structure)
5. Apply inverse FFT to reconstruct the denoised image
6. Plot and save the results

---

## 🧩 Code Walkthrough (What Each Part Does)

### 1) Import libraries
```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
```
- NumPy: FFT + array operations
- Matplotlib: plotting
- imread: image loading

---

### 2) Load and preprocess image
```python
img = imread("Final/AlternativeAssessment.png")

if img.ndim == 3:
    img = img.mean(axis=2)
```
- Loads the scanned image
- Converts RGB → grayscale by averaging channels
- Ensures the image is a 2D array for 2D FFT

---

### 3) Apply 2D FFT
```python
F = np.fft.fft2(img)
F_shift = np.fft.fftshift(F)
magnitude = np.log(1 + np.abs(F_shift))
```
- fft2: transform image to frequency domain
- fftshift: move DC term to the center
- log(1+|F|): compress dynamic range so peaks are easier to see
>Note: The log scaling is mainly for visibility and stable peak detection.

---

### 4) Create a frequency mask + threshold
```python
rows, cols = img.shape
crow, ccol = rows // 2, cols // 2

mask = np.ones_like(img)
threshold = 0.6 * magnitude.max()
```
- mask = 1: keep all frequencies initially
- threshold: identifies unusually strong frequency components (likely periodic noise)
🔍 Why threshold = 0.6 × max?
- Periodic noise creates very strong peaks compared to normal image frequencies
- Using a fraction of the maximum isolates only dominant outliers=- 0.6 is an empirical balance:
    - too low → removes real image detail (over-filtering)
    - too high → leaves grid noise (under-filtering)

---

### 5) Suppress noise peaks (while preserving the center)
```python
for i in range(rows):
    for j in range(cols):
        if magnitude[i, j] > threshold:
            if np.sqrt((i - crow)**2 + (j - ccol)**2) > 15:
                mask[i, j] = 0
```
This does two things:
1. Peak condition: magnitude[i, j] > threshold
- targets only strong frequency peaks (suspected noise)
2. Radius protection: distance > 15
- preserves a circular region near the center (DC + low frequencies)
- prevents shifts in overall brightness and keeps major image structure

---

### 6) Inverse FFT (reconstruction)
```python
F_filtered = F_shift * mask
F_ishift = np.fft.ifftshift(F_filtered)
img_denoised = np.fft.ifft2(F_ishift)
img_denoised = np.real(img_denoised)
```
- Apply mask in frequency space
- Transform back to spatial domain
- Take real part (imaginary part is numerical error)

---

### 7) Visualize and save results
```python
plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
plt.imshow(img, cmap="gray")
plt.title("Original Noisy Image")
plt.axis("off")

plt.subplot(1,3,2)
plt.imshow(magnitude, cmap="gray")
plt.title("FFT Magnitude Spectrum")
plt.axis("off")

plt.subplot(1,3,3)
plt.imshow(img_denoised, cmap="gray")
plt.title("Denoised Image (FFT)")
plt.axis("off")

plt.tight_layout()
plt.savefig("output.png", dpi=300, bbox_inches="tight")
plt.show()
```
