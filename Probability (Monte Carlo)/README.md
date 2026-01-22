# Chapter 5 — Probability (Monte Carlo)

This folder contains small Python scripts for **Monte Carlo (MC) integration**, **sampling**, **Markov Chain Monte Carlo (MCMC)**, and a **2D Ising model** simulated using the **Metropolis algorithm** (SIF3012 Computational Physics — Chapter 5).

The goal is to show:
- how MC estimates integrals by random sampling,
- why MC error decreases slowly as ~ 1/sqrt(N),
- why MC becomes useful for higher-dimensional problems,
- how Metropolis builds a Markov chain for sampling physical distributions.

---

## Contents

### 1) 1D Monte Carlo Integration
- **`Monte_Carlo_1D.py`**
  - Integrates **f(x) = x²** on **[0,1]**
  - Compares:
    - Midpoint rule (single-panel)
    - Trapezoid rule (single-panel)
    - Simpson’s rule (SciPy)
    - Monte Carlo integration (uniform sampling)
  - Saves: `Monte-Carlo_1D.png`

- **`montecarlo.py`**
  - Integrates **f(x) = sin(x) + 1** on **[0, 1.5π]**
  - Compares Simpson vs MC
  - Produces a plot (no file save in current version)

### 2) Sampling / Expectation Under a PDF
- **`sampling.py`**
  - Samples **x ~ Normal(0,1)**
  - Estimates **E[1 + x²]** using the sample mean
  - Also computes the same expectation using Simpson integration of:
    (1 + x²) * exp(-x²/2) / sqrt(2π) over a truncated range [-5,5]
  - Visualizes the integrand + sampled points

### 3) 2D Monte Carlo Integration (Double Integral)
- **`Monte_Carlo_double_integral.py`**
  - Computes ∬ (x + y) dx dy over the unit square [0,1]×[0,1]
  - Uses:
    - SciPy `dblquad` as a reference
    - Monte Carlo sampling for the estimate
  - Saves: `Monte_Carlo_double_integral.png`

### 4) Markov Chain Monte Carlo (Metropolis)
- **`mcmc.py`**
  - Demonstrates random-walk Metropolis sampling for a 1D target:
    π(x) ∝ 1/(1 + x²) on (0,3)
  - Outputs a histogram of the sampled chain

### 5) Statistical Physics Application: 2D Ising Model
- **`ising_model.py`**
  - Simulates a 2D Ising lattice (L×L spins ±1) at temperature T
  - Uses Metropolis updates with periodic boundary conditions
  - Plots:
    - initial spin configuration
    - final configuration
    - energy vs Monte Carlo steps

---

## Requirements

Python 3.9+ recommended.

Install dependencies:
```bash
pip install numpy matplotlib scipy
```

---

## Running

```bash
python Monte_Carlo_1D.py
python Monte_Carlo_double_integral.py
python sampling.py
python mcmc.py
python ising_model.py
```

---

## What the Code Is Doing (High-Level)

### Monte Carlo Integration (Uniform Sampling)

To estimate the definite integral:

\[
I = \int_a^b f(x)\, dx
\]

we draw random samples:

\[
x_i \sim U(a, b)
\]

and approximate the integral as:

\[
I \approx (b - a)\,\frac{1}{N}\sum_{i=1}^{N} f(x_i)
\]

The statistical error of Monte Carlo integration typically decreases as:

\[
\Delta I \propto \frac{1}{\sqrt{N}}
\]

This slow convergence rate is independent of the dimension of the integral, which makes Monte Carlo methods especially useful for high-dimensional problems.

---

### 2D Monte Carlo Integration

For a rectangular domain with total area \(A\), the double integral

\[
I = \iint f(x, y)\, dx\, dy
\]

can be approximated by uniformly sampling points \((x_i, y_i)\) inside the domain:

\[
(x_i, y_i) \sim U(\text{domain})
\]

The Monte Carlo estimate is then:

\[
I \approx A \cdot \frac{1}{N}\sum_{i=1}^{N} f(x_i, y_i)
\]

As in the one-dimensional case, the statistical uncertainty scales as:

\[
\Delta I \propto \frac{1}{\sqrt{N}}
\]

---

### Key Characteristics of Monte Carlo Integration

- The convergence rate does **not depend on dimension**
- Accuracy improves slowly, requiring large \(N\) for high precision
- Particularly effective when:
  - the integration domain is high-dimensional
  - the integrand is complicated or discontinuous
  - deterministic quadrature becomes impractical

---

### Limitations

- Monte Carlo methods are statistically noisy
- Doubling accuracy requires approximately **four times** more samples
- Error estimates rely on correct variance calculation of the integrand
- Results vary between runs unless a fixed random seed is used, e.g,
```python
np.random.seed(0)
```

