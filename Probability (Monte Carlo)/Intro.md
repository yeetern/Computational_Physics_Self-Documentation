# Summary Report — Monte Carlo Integration (Tutorial 5)

## Problem Statement

This group assignment is based on **Tutorial 5: Monte Carlo** from the course **SIF3012 Computational Physics (Semester 1, 2025/2026)**.  
Each group is assigned a two-dimensional function \( f(x, y) \) defined on the square domain  
\[
(x, y) \in [0,1] \times [0,1].
\]

The task is to compute the integral
\[
I = \int_0^1 \int_0^1 f(x, y)\, dx\, dy
\]
using Monte Carlo sampling, and to analyze the statistical properties of the estimate.

Specifically, the questions require us to:
1. Estimate the integral using Monte Carlo sampling.
2. Study how the estimate converges as the number of samples \(N\) increases.
3. Estimate the statistical uncertainty and verify the expected \(1/\sqrt{N}\) scaling.
4. Compare the Monte Carlo result with the expected (reference) value.
5. Comment on the convergence behavior of the integrand. :contentReference[oaicite:0]{index=0}

---

## Methodology and Code Implementation

### Monte Carlo Estimation of the Integral

To estimate the two-dimensional integral, the code generates \(N\) random sample points
\[
(x_i, y_i) \sim U([0,1] \times [0,1])
\]
using NumPy’s uniform random number generator.  
The Monte Carlo estimator for the integral is given by:
\[
I_N = \frac{1}{N} \sum_{i=1}^{N} f(x_i, y_i),
\]
since the area of the integration domain is unity.

This directly fulfills the requirement to compute the integral using Monte Carlo sampling.

---

### Convergence Study

To study convergence, the code evaluates the Monte Carlo estimate \(I_N\) for increasing values of \(N\).  
The estimate is plotted as a function of \(N\), allowing us to observe how the numerical result approaches the expected value as the sample size increases.

This satisfies the requirement to analyze convergence behavior as a function of the number of samples.

---

### Statistical Uncertainty and Error Scaling

The statistical uncertainty of the Monte Carlo estimate is computed using the standard error:
\[
\sigma_N = \frac{\sqrt{\langle f^2 \rangle - \langle f \rangle^2}}{\sqrt{N}},
\]
where the averages are taken over the sampled points.

By plotting the estimated error against \(N\) on a log-log scale, the expected
\[
\sigma_N \propto \frac{1}{\sqrt{N}}
\]
behavior is verified. This confirms the theoretical scaling of Monte Carlo uncertainty.

---

### Comparison with the Expected Value

A high-accuracy reference value for the assigned function is provided in the tutorial.  
The Monte Carlo estimates are compared against this expected value, and the deviation decreases as \(N\) increases.

The number of samples required to achieve approximately **1% accuracy** is determined by identifying when the Monte Carlo estimate lies within 1% of the reference value.

---

### Convergence Behavior of the Integrand

The convergence behavior depends on the smoothness and variance of the integrand \(f(x,y)\).  
For smooth functions with bounded variance, convergence is steady but slow, following the characteristic Monte Carlo rate of \(1/\sqrt{N}\).  
Fluctuations in the estimate at small \(N\) are expected due to statistical noise and diminish as more samples are used.

---

## Limitations

While Monte Carlo integration is simple and robust, it has several limitations:
- Convergence is slow compared to deterministic methods for low-dimensional smooth integrals.
- A large number of samples is required to achieve high precision.
- Results exhibit statistical fluctuations and vary between runs unless a fixed random seed is used.
- Error estimates rely on accurate variance estimation, which can itself be noisy for small \(N\).

---

## Possible Improvements

Several improvements could be made to enhance the analysis:
- Use of variance reduction techniques such as importance sampling or stratified sampling.
- More systematic determination of the sample size required for a given accuracy.
- Averaging results over multiple independent Monte Carlo runs.
- Extending the analysis to higher-dimensional integrals where Monte Carlo methods provide clearer advantages.

---

## Conclusion

- This assignment demonstrates how Monte Carlo sampling can be used to estimate two-dimensional integrals and analyze their statistical properties.  
- The implemented code fulfills all requirements of the tutorial by estimating the integral, studying convergence, quantifying statistical uncertainty, and comparing results with known reference values.  
- The results clearly illustrate both the strengths and limitations of Monte Carlo integration as a numerical method in computational physics.
