# Euler Method — Logistic Equation (SIF3012, Block 1)

**Course:** SIF3012 Computational Physics  
**Lecturer:** Juan Carlos Algaba  
**Problem type:** Initial Value Problem (IVP), Ordinary Differential Equation (ODE)

We study the logistic differential equation:
\[
\frac{dy}{dt} = 2y(1-y)
\]

---

## 1. Problem Overview

The initial condition is defined as:
\[
y_0 = \frac{\text{last two digits of metric number}}{100}
\]

Tasks:
1. Manual Euler calculation using \( h = 0.125 \).
2. Python Euler implementation with \( h = 0.125 \).
3. Python Euler implementation with \( h = 0.00125 \).
4. Plot numerical results and compare accuracy.

---

## 2. What We Learn (Key Takeaways)

### (a) Euler Method as a First-Order Integrator

Euler update rule:
\[
y_{n+1} = y_n + h f(y_n)
\]

Assumptions:
- The slope is approximately constant over one time step.
- The step size \( h \) is sufficiently small.

Properties:
- Simple and intuitive
- Computationally cheap
- Global error scales as \( \mathcal{O}(h) \)

---

### (b) Step Size Controls Accuracy

Comparing:
- \( h = 0.125 \) (coarse)
- \( h = 0.00125 \) (fine)

Observations:
- Coarse steps lag behind the analytical solution.
- Fine steps closely track the true trajectory.

This demonstrates numerical convergence.

---

### (c) Dependence on Initial Condition \( y_0 \)

- \( y_0 = 0.01 \): steep transient → larger numerical error
- \( y_0 = 0.50 \): closer to equilibrium → smaller visible error

Numerical stability depends on both dynamics and step size.

---

## 3. Code Structure and How It Works

### Core Components

| Component | Purpose |
|---------|--------|
| `f(y)` | Defines the ODE |
| `euler(y0, h, tf)` | Euler integrator |
| `y_exact(t, y0)` | Analytical solution |
| CLI (`argparse`) | Flexible input |
| Matplotlib | Visualization |

---

### Generic Euler Solver

```python
def euler(y0, h, tf):
    n = int(round(tf / h))
    y = y0
    t = 0.0
    ts = [t]
    ys = [y]

    for _ in range(n):
        y = y + h * f(y)
        t += h
        ts.append(t)
        ys.append(y)

    return np.array(ts), np.array(ys)
```

---
## 4. When Should You Use Euler Method?

### ✅ Use Euler when:
- you want conceptual understanding,
- you need a quick numerical sanity check,
- the time step is very small,
- the system is non-stiff and smooth.

### ❌ Avoid Euler when:
- high precision is required,
- the system is stiff,
- long-time integration is needed,
- the slope changes rapidly.

Prefer:
- Runge–Kutta methods (RK2, RK4),
- Adaptive solvers (`scipy.integrate.solve_ivp`).

## 5. Numerical Limitations (Important Insight)

From numerical experiments and instructor feedback:

- Large initial values or large step sizes can cause numerical failure
- Euler method cannot accurately track rapidly changing slopes
- This behavior is **not a bug**, but a **methodological limitation**

> **Key principle:**  
> Numerical methods can fail silently if their underlying assumptions are violated.

For explicit Euler, the assumption of locally constant slope breaks down when:
- the solution grows or decays rapidly,
- the step size is too large relative to the system’s timescale.

Understanding *why* a method fails is more important than simply avoiding failure.

---

## 6. About Input Handling (Engineering vs Physics)

### Current behavior
- Input `l2d` → `y0 = l2d / 100`
- Input like `1234` → `y0 = 12.34`

### Is this a problem?

**Physics perspective:**
- The valid input domain is defined by the physical model.
- If the model assumes \( 0 < y_0 < 1 \), inputs outside this range are unphysical.
- Garbage input → garbage physics.

**Engineering perspective:**
- Input sanitization improves robustness and user experience.
- Warnings or constraints can prevent misleading numerical results.

For coursework and research prototyping:

> **Correct physics > defensive programming**

However, minimal validation (e.g. warnings for unphysical \( y_0 \)) can be useful.

---

## 7. How to Reuse This Code in the Future

### (a) Change the ODE

Replace:

```python
def f(y):
    return 2*y*(1-y)
```

with any other function `f(y)`.

Examples:

- **Exponential decay:**  
  `f(y) = -k * y`

- **Logistic equation with different growth rate:**  
  `f(y) = r * y * (1 - y)`

- **Simple rate equations** in chemistry or plasma physics

---

### (b) Extend to Time-Dependent Systems

With a minor refactor, the solver can handle time-dependent equations \( f(t, y) \):

- Change the function signature to `f(t, y)`
- Update the Euler step to  
  `y = y + h * f(t, y)`

This allows modeling of:

- driven systems,
- external forcing,
- time-varying parameters.

---

### (c) Use as a Baseline Solver

This Euler implementation is useful as:

- a baseline for comparison with higher-order methods (RK2, RK4),
- a tool to study numerical convergence,
- a teaching reference for stability and error growth.

Because Euler’s method is explicit and simple, deviations from the exact solution
are easy to interpret physically.

---

## Instructor Feedback (Excerpt)

> “Code seems fine, feel free to upload to GitHub for future reference.  
> Once the initial value becomes large, Euler’s approximation is no longer sufficient  
> to keep with the function slope.”
>
> — **Dr. Juan Carlos Algaba**, SIF3012 Computational Physics

**Interpretation:**  
Unexpected behavior at large initial values or large step sizes arises from the
first-order nature of the Euler method and the defined input rule, not from a coding error.

---

## Summary

This assignment highlights that:

- numerical accuracy depends critically on step size,
- initial conditions influence error growth,
- numerical methods must always be interpreted through their assumptions.

The Euler method is best viewed as a **conceptual and diagnostic tool**, rather than
a high-precision numerical solver.

---

## Possible Extensions

- Implement Runge–Kutta (RK4) and compare error scaling
- Investigate stability limits by increasing the step size
- Generalize the solver to systems of coupled ODEs
