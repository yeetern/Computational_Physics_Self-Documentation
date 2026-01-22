# SIF3012 — Chapter 5: Probability (Monte Carlo)
## Final Exam Cheat Sheet

---

## 1. What Questions Usually Ask

Typical Monte Carlo questions require you to:

1. **Estimate an integral using Monte Carlo sampling**
2. **Study convergence as number of samples N increases**
3. **Estimate statistical uncertainty**
4. **Verify 1/√N error scaling**
5. **Compare with expected / exact value**
6. **Comment on convergence behavior**
7. (Sometimes) **Determine N needed for ~1% accuracy**

These appear for:
- 1D integrals
- 2D integrals over a square
- Probability expectations
- Metropolis / MCMC (conceptual + algorithmic)
- Ising model (conceptual + acceptance rule)

---

## 2. Core Monte Carlo Integration (1D)

### Problem Form
\[
I = \int_a^b f(x)\,dx
\]

### Monte Carlo Estimator
Sample:
\[
x_i \sim U(a,b)
\]

Estimate:
\[
I_N = (b-a)\frac{1}{N}\sum_{i=1}^N f(x_i)
\]

### Statistical Error
\[
\sigma_I = (b-a)\frac{\sqrt{\langle f^2\rangle - \langle f\rangle^2}}{\sqrt{N}}
\]

### Key Result (Must Remember)
\[
\boxed{\sigma \propto \frac{1}{\sqrt{N}}}
\]

---

### Code Pattern (1D)
```python
x = np.random.uniform(a, b, N)
f = func(x)

I = (b - a) * np.mean(f)
error = (b - a) * np.std(f) / np.sqrt(N)
```

---

## 3. Monte Carlo Integration (2D — Exam Favorite)

### Problem Form

We are given a two-dimensional integral over the unit square:

\[
I = \int_0^1 \int_0^1 f(x, y)\, dx\, dy
\]

### Domain Area

Since the integration domain is \([0,1] \times [0,1]\),

\[
A = 1
\]

---

### Monte Carlo Estimator

We generate \(N\) random points uniformly in the square:

\[
(x_i, y_i) \sim U([0,1] \times [0,1])
\]

The Monte Carlo estimate of the integral is:

\[
I_N = \frac{1}{N}\sum_{i=1}^{N} f(x_i, y_i)
\]

---

### Statistical Error

The statistical uncertainty of the Monte Carlo estimate is given by:

\[
\sigma = \frac{\sqrt{\langle f^2 \rangle - \langle f \rangle^2}}{\sqrt{N}}
\]

where the averages are taken over the sampled points.

This shows that the Monte Carlo error decreases as:

\[
\sigma \propto \frac{1}{\sqrt{N}}
\]

---

### Convergence Behavior

As the number of samples \(N\) increases:

- The Monte Carlo estimate \(I_N\) fluctuates around the expected value
- The magnitude of fluctuations decreases with increasing \(N\)
- Convergence is slow compared to deterministic methods, but robust

This \(1/\sqrt{N}\) convergence rate is **independent of dimensionality**, which is why Monte Carlo methods are especially useful for high-dimensional integrals.

---

### Typical Exam Tasks

For this type of problem, you are usually asked to:

1. Compute the Monte Carlo estimate of the integral
2. Plot \(I_N\) as a function of \(N\)
3. Estimate the statistical error
4. Verify the \(1/\sqrt{N}\) error scaling
5. Compare with the expected (exact or reference) value
6. Estimate how many samples are required to achieve approximately 1% accuracy

---

### Code Skeleton (2D Monte Carlo Integration)

```python
import numpy as np

N = 10000

# Uniform sampling in [0,1] x [0,1]
x = np.random.rand(N)
y = np.random.rand(N)

# Define integrand
f = func(x, y)

# Monte Carlo estimate
I = np.mean(f)

# Statistical error
error = np.sqrt(np.mean(f**2) - np.mean(f)**2) / np.sqrt(N)

print("Integral estimate:", I)
print("Statistical error:", error)
```

---

## 4. Convergence Study (Very Common)

### What Examiner Wants

- Show Monte Carlo estimate → expected value
- As \(N\) increases, fluctuations decrease
- Error \( \propto \frac{1}{\sqrt{N}} \)

---

### What You Do

- Compute \(I_N\) for increasing \(N\)
- Plot \(I_N\) vs \(N\)
- Plot error vs \(N\) (log–log if asked)

---

### Code Pattern

```python
N_list = [100, 500, 1000, 5000, 10000]
I_list = []
err_list = []

for N in N_list:
    x = np.random.rand(N)
    y = np.random.rand(N)
    f = func(x, y)

    I_list.append(np.mean(f))
    err_list.append(np.std(f) / np.sqrt(N))
```

---

## 5. 1% Accuracy Question (Almost Guaranteed)

### Meaning

The requirement for 1% accuracy is:

\[
\frac{\left| I_N - I_{\text{exact}} \right|}{I_{\text{exact}}} \lesssim 0.01
\]

This means that the relative error of the Monte Carlo estimate must be less than approximately 1%.

---

### Rule of Thumb

Since the Monte Carlo statistical error scales as:

\[
\sigma \sim \frac{1}{\sqrt{N}}
\]

to reduce the error by a factor of 10, the number of samples must be increased by a factor of 100.

\[
\text{Error} \downarrow \times 10
\quad \Rightarrow \quad
N \uparrow \times 100
\]

---

## 6. Expected Value / Probability Sampling

### Expectation Definition

The expectation value of a function \( g(x) \) with respect to a probability density \( p(x) \) is defined as:

\[
\mathbb{E}[g(x)] = \int g(x)\, p(x)\, dx
\]

---

### Monte Carlo Estimator

To estimate the expectation value using Monte Carlo sampling:

Sample:
\[
x_i \sim p(x)
\]

Estimate:
\[
\mathbb{E}[g(x)] \approx \frac{1}{N}\sum_{i=1}^{N} g(x_i)
\]

---

### Code Pattern

```python
x = np.random.normal(0, 1, N)
g = 1 + x**2

expectation = np.mean(g)
```

---

## 7. Markov Chain Monte Carlo (Metropolis)

### When Used

Markov Chain Monte Carlo (MCMC) methods are used when:

- The target distribution is **non-uniform**
- Direct sampling from the distribution is **not possible**

---

### Metropolis Algorithm (Must Memorize)

1. Start with an initial state \( x \)
2. Propose a new state:
   \[
   x' = x + \delta
   \]
3. Compute the acceptance probability:
   \[
   \alpha = \min\left(1, \frac{\pi(x')}{\pi(x)}\right)
   \]
4. Accept the proposal if a random number \( r < \alpha \)

If accepted, set \( x \leftarrow x' \); otherwise, keep the current state.

---

### Key Exam Points

- Generated samples are **correlated**
- A **burn-in** period is required to reach equilibrium
- Effective sample size is smaller than the total number of steps
- The stationary distribution of the Markov chain equals the target distribution

---

### Code Skeleton

```python
for i in range(steps):
    proposal = x + np.random.uniform(-d, d)
    alpha = min(1, pi(proposal) / pi(x))

    if np.random.rand() < alpha:
        x = proposal

    samples.append(x)
```

---

## 8. Ising Model (Metropolis in Physics)

### Energy

The energy of a two-dimensional Ising model with nearest-neighbor interactions is given by:

\[
E = -J \sum_{\langle i,j \rangle} s_i s_j
\]

where \( s_i = \pm 1 \) represents the spin at lattice site \( i \), and the sum runs over nearest-neighbor pairs.

---

### Spin Flip Rule

When a single spin is flipped, the change in energy is:

\[
\Delta E = E_{\text{new}} - E_{\text{old}}
\]

The proposed spin flip is accepted if:

\[
\Delta E \le 0
\quad \text{or} \quad
e^{-\Delta E/(kT)} > r
\]

where \( r \in (0,1) \) is a uniformly distributed random number.

---

### What Examiner Wants

- Clear connection to the **canonical ensemble**
- Understanding that Monte Carlo sampling generates **equilibrium configurations**
- Interpretation of **energy versus Monte Carlo steps**
- Conceptual discussion of **phase transition behavior**

---

## 9. Common Exam Comments (Memorize These)

### Why Monte Carlo?

- Dimension-independent convergence
- Works well for complex or high-dimensional integrals where deterministic methods fail

---

### Limitations

- Slow convergence rate \( \sim 1/\sqrt{N} \)
- Statistical noise in the estimates
- Requires a large number of samples for high accuracy
- Samples generated by MCMC methods are correlated

---

### Improvements

- Importance sampling
- Stratified sampling
- Variance reduction techniques
- Better proposal distributions in MCMC
- Cluster algorithms for the Ising model

---

## 10. One-Sentence Killer Summary (Exam Gold)

> Monte Carlo methods estimate integrals and expectations using random sampling, with statistical uncertainty decreasing as \(1/\sqrt{N}\), making them inefficient for low-dimensional smooth problems but powerful for high-dimensional and complex systems.
