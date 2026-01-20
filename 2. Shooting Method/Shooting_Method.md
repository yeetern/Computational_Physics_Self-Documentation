# Shooting Method for Boundary Value Problems (SIF3012, Block 2)

**Course:** SIF3012 Computational Physics  
**Lecturer:** Juan Carlos Algaba  
**Problem type:** Boundary Value Problem (BVP), Second-Order ODE  

This block focuses on solving a **boundary value problem** using the **Shooting Method**, combined with **Euler’s method** for numerical integration.

The official problem statement is given in the course handout :contentReference[oaicite:0]{index=0}.

---

## 1. Problem Overview

We consider the second-order ordinary differential equation

\[
y'' + x y' - x y = 2x
\]

subject to the boundary conditions

\[
y(0) = 1, \qquad y(2) = 8.
\]

### Objectives
1. Convert the second-order ODE into two first-order ODEs.
2. Apply the **Shooting Method** with step size \( h = 0.1 \).
3. Determine the correct initial slope \( y'(0) \).
4. Plot the resulting numerical solution.

---

## 2. Reduction to a First-Order System

To apply standard IVP solvers, the second-order ODE is rewritten as a system of first-order equations.

Define
\[
z = \frac{dy}{dx}.
\]

Then the system becomes
\[
\begin{aligned}
\frac{dy}{dx} &= z, \\
\frac{dz}{dx} &= 2x - xz + xy.
\end{aligned}
\]

This reformulation allows the use of Euler’s method for numerical integration.

---

## 3. Shooting Method: Core Idea

Boundary value problems cannot be solved directly using standard initial value solvers.

The **Shooting Method** works by:
1. Guessing an initial slope \( s = y'(0) \),
2. Solving the IVP from \( x = 0 \) to \( x = 2 \),
3. Comparing the computed value \( y(2; s) \) with the target value \( y(2) = 8 \),
4. Iteratively updating \( s \) until the boundary condition is satisfied.

Define the mismatch function
\[
F(s) = y(2; s) - 8.
\]

The correct initial slope satisfies \( F(s) = 0 \).

---

## 4. Secant Method for Updating the Initial Slope

To find the root of \( F(s) \), the **Secant Method** is used.

Given two initial guesses \( s_1 \) and \( s_2 \),
\[
s_{k+1} = s_k - F(s_k)\frac{s_k - s_{k-1}}{F(s_k) - F(s_{k-1})}.
\]

### Key observations
- No derivative of \( F(s) \) is required.
- For this problem, \( F(s) \) is nearly linear in \( s \), so convergence is very fast (often one iteration).

---

## 5. Numerical Accuracy and Limitations

### Euler Method
- First-order accurate in step size \( h \),
- Simple and intuitive,
- Accuracy is limited when embedded inside the shooting method.

With \( h = 0.1 \), the computed initial slope deviates noticeably from a high-accuracy reference.

### Shooting Method Sensitivity
- If both guesses undershoot or overshoot, convergence may slow or fail.
- Integration error directly propagates into the estimated slope.

> Boundary value problems amplify numerical errors more strongly than IVPs.

---

## 6. Comparison with Higher-Order Methods (Additional Study)

For deeper understanding, the Euler-based shooting solution was compared with a **Runge–Kutta 4th order (RK4)** implementation using a very small step size.

Key findings:
- RK4 achieves high accuracy with far fewer steps.
- Euler requires extremely small \( h \) to match RK4 accuracy.
- Error scaling:
  - Euler: global error \( \mathcal{O}(h) \),
  - RK4: global error \( \mathcal{O}(h^4) \).

This highlights the trade-off between **conceptual simplicity** and **computational efficiency**.

---

## 7. When Should You Use the Shooting Method?

### Suitable when:
- The problem is a two-point BVP,
- The ODE is smooth and not highly stiff,
- Reasonable initial slope guesses are available.

### Limitations:
- Sensitive to integration errors,
- Less effective for stiff or highly nonlinear systems,
- Can fail if \( s \mapsto y(2; s) \) is not smooth.

---

## 8. Core Code (Reference Implementation)

This section collects the **minimal, reusable core code** for the shooting method.  
It is intended for **future learning, revision, and reuse**, independent of plotting
or extended accuracy comparisons.

---

### 8.1 Problem Setup

```python
h = 0.1
x0, xf = 0.0, 2.0
N = int((xf - x0) / h)

y0 = 1.0
yf = 8.0
```

### 8.2 ODE Definition

```python
def f1(x, y, z):
    return z

def f2(x, y, z):
    return 2*x - x*z + x*y
```

### 8.3 Euler Integrator for a Given Initial Slope

```python
def euler(s):
    x = x0
    y = y0
    z = s

    xs = [x]
    ys = [y]

    for _ in range(N):
        dy = f1(x, y, z)
        dz = f2(x, y, z)

        y = y + h * dy
        z = z + h * dz
        x = x + h

        xs.append(x)
        ys.append(y)

    return xs, ys, y
```

### 8.4 Shooting Method

```python
def F(s):
    _, _, y_end = euler(s)
    return y_end - yf
```

### 8.5 Secant Method

```python
def shooting_secant(s1, s2, tol=1e-6, i_max=50):
    F1 = F(s1)
    F2 = F(s2)

    for _ in range(i_max):
        if abs(F2 - F1) < 1e-14:
            break

        s3 = s2 - F2 * (s2 - s1) / (F2 - F1)
        F3 = F(s3)

        if abs(F3) < tol:
            return s3

        s1, s2 = s2, s3
        F1, F2 = F2, F3

    return s2
```

### 8.6 Typical Usage

```python
s_guess1 = 1.0
s_guess2 = 3.0

s_star = shooting_secant(s_guess1, s_guess2)
xs, ys, y_end = euler(s_star)

print("Optimal initial slope:", s_star)
print("y(2) ≈", y_end)
```

---
## 9. Instructor Feedback (Excerpt)

>“Very nice that you allow the user to input their own guessing parameters.
Allows to play and see what happens for many non pre-defined scenarios.”
— Dr. Juan Carlos Algaba, SIF3012 Computational Physics

Interpretation:
Allowing flexible initial guesses strengthens intuition about undershoot, overshoot,
and convergence behavior in boundary value problems.

---

## 10. Summary

Block 2 demonstrates that:
- Boundary value problems require different strategies than IVPs,
- The shooting method converts a BVP into a root-finding problem,
- Numerical accuracy of the integrator is critical,
- Higher-order methods are far more efficient for practical computation.

This block builds a strong foundation for real-world numerical modeling in physics.