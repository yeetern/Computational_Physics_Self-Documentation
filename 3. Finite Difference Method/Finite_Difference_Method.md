# Finite Difference Method for Boundary Value Problems (SIF3012, Block 3)

**Course:** SIF3012 Computational Physics  
**Lecturer:** Juan Carlos Algaba  
**Problem type:** Boundary Value Problem (BVP), Second-Order ODE  

This block applies the **Finite Difference Method (FDM)** to solve a second-order boundary value problem and studies how **step size** and **discretization choice** (forward, backward, central) affect numerical accuracy and stability.

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
1. Solve the BVP using the finite difference method with step size \( h = 0.5 \).
2. Explicitly construct and display the linear system \( A\mathbf{y} = \mathbf{b} \).
3. Repeat the computation with a finer step size \( h = 0.01 \).
4. Plot and compare the numerical solutions.

---

## 2. Finite Difference Discretization

The finite difference method replaces derivatives by algebraic approximations on a grid

\[
x_i = x_0 + i h, \quad i = 0, 1, \dots, N.
\]

Different discretization choices lead to different numerical behavior:

- **Forward difference**: biased, first-order accurate  
- **Backward difference**: biased, first-order accurate  
- **Central difference**: symmetric, second-order accurate  

These choices directly affect truncation error and stability.

---

## 3. Linear System Formulation

Applying finite differences at interior grid points transforms the ODE into a linear system

\[
A \mathbf{y} = \mathbf{b},
\]

where:
- \( A \) is the finite-difference matrix,
- \( \mathbf{y} \) contains the unknown interior values,
- \( \mathbf{b} \) includes the forcing term and boundary contributions.

Boundary values \( y(0) \) and \( y(2) \) are enforced explicitly.

---

## 4. Numerical Accuracy and Method Comparison

### Coarse grid: \( h = 0.5 \)
- Small matrix, easy to inspect.
- Large truncation error.
- Forward and backward schemes show strong bias.
- Central difference gives noticeably better accuracy.

### Fine grid: \( h = 0.01 \)
- Much larger system.
- Truncation error significantly reduced.
- Numerical solution converges toward the reference solution.

> Reducing the step size improves accuracy but increases computational cost.

---

## 5. Key Observations

- Central differences outperform forward and backward schemes at the same step size.
- Large discrepancies at coarse resolution arise from truncation error, not coding mistakes.
- Numerical convergence is controlled jointly by:
  - discretization order,
  - step size,
  - problem smoothness.

This explains why central, backward, and forward schemes can give **very different solutions** when \( h \) is large, as noted in instructor feedback.

---

## 6. Core Code (Reference Implementation)

This section contains the **essential finite difference structure** for future learning, revision, and reuse.   Experimental printouts and plotting details are omitted for clarity.

---

### 6.1 Problem Setup

```python
import numpy as np

h = 0.5
x0, xN = 0.0, 2.0
y0, yN = 1.0, 8.0

x = np.arange(x0, xN + h/2, h)
N = len(x) - 1
m = N - 1    # number of interior unknowns
```

### 6.2 Central Difference Scheme

```python
def central_difference(x, h, y0, yN):
    N = len(x) - 1
    m = N - 1
    A = np.zeros((m, m))
    b = np.zeros(m)

    for i in range(m):
        j = i + 1
        xj = x[j]

        c_jm1 = 1/h**2 - xj/(2*h)
        c_j   = -2/h**2 - xj
        c_jp1 = 1/h**2 + xj/(2*h)
        rhs   = 2 * xj

        if j-1 >= 1:
            A[i, j-2] += c_jm1
        else:
            b[i] -= c_jm1 * y0

        A[i, j-1] += c_j

        if j+1 <= N-1:
            A[i, j] += c_jp1
        else:
            b[i] -= c_jp1 * yN

        b[i] += rhs

    return A, b
```

### 6.3 Solving Linear System

```python
A, b = central_difference(x, h, y0, yN)
y_int = np.linalg.solve(A, b)

y = np.zeros(N + 1)
y[0] = y0
y[-1] = yN
y[1:-1] = y_int
```

## Notes for future reuse
- Replace coefficients to solve other second-order linear ODEs.

- Increase order of accuracy using higher-order finite differences.

- Extend to nonlinear problems using iterative solvers.

- Combine with sparse matrix techniques for large grids.

---

## 7. Instructor Feedback (Excerpt)
>“I’m surprised the central, backward methods are giving so different solutions. It would have been interesting to compare if such large errors also happen when the step is much smaller, and what limiting step we can accept.”
— Dr. Juan Carlos Algaba, SIF3012 Computational Physics

Interpretation:
The observed discrepancies are a direct consequence of truncation error and discretization bias. Reducing the step size and using higher-order schemes restores consistency between methods.

---

## 8. Summary
Block 3 demonstrates that:
- Finite difference methods convert differential equations into linear algebra problems.
- Discretization choice matters as much as step size.
- Central differences provide superior accuracy at the same resolution.
- Numerical methods must be analyzed, not trusted blindly.

This block completes the conceptual progression:
Euler → Shooting → Finite Differences, forming a solid foundation for computational physics and numerical modeling.