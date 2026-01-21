#Alternative Assessment 1 Question 2
#Program Name: FFT on Lily png
#Subject: SIF3012 Computational Physics
#Author: Tan Yee Tern
#Student ID: 23006131
#Email: 23006131@siswa.um.edu.my
#Date of Creation: Tuesday Jan 20

#--------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

# Load image (grayscale)
img = imread("Final/AlternativeAssessment.png") # My directory (Sub folder "Final")

# If RGB, convert to grayscale
if img.ndim == 3:
    img = img.mean(axis=2)

# 2D FFT
F = np.fft.fft2(img)
F_shift = np.fft.fftshift(F)
magnitude = np.log(1 + np.abs(F_shift))

# Create frequency mask
rows, cols = img.shape
crow, ccol = rows // 2, cols // 2

mask = np.ones_like(img)

# Threshold to detect strong periodic noise peaks
threshold = 0.6 * magnitude.max()

# Remove high peaks except the center
for i in range(rows):
    for j in range(cols):
        if magnitude[i, j] > threshold:
            if np.sqrt((i - crow)**2 + (j - ccol)**2) > 15:
                mask[i, j] = 0

# Apply mask and inverse FFT
F_filtered = F_shift * mask
F_ishift = np.fft.ifftshift(F_filtered)
img_denoised = np.fft.ifft2(F_ishift)
img_denoised = np.real(img_denoised)

# Plot results
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
