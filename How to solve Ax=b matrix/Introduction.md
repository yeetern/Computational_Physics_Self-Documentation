# Solving Linear Systems of Equations (Gaussian Elimination & LU Decomposition)

**Course:** Computational Physics  
**Lecturer:** Dr. Norhasliza  
**Topic:** Linear algebra methods for solving \( A\mathbf{x} = \mathbf{b} \)

This section documents multiple numerical methods for solving a system of linear equations,
implemented **from first principles** and verified against NumPy’s built-in solver.

---

## 1. Problem Overview

We consider the linear system

\[
A \mathbf{x} = \mathbf{b},
\]

where

\[
A =
\begin{pmatrix}
21 & 67 & 88 & 73 \\
76 & 63 & 70 & 20 \\
0 & 85 & 560 & 54 \\
193 & 43 & 30.2 & 29.4
\end{pmatrix},
\quad
\mathbf{b} =
\begin{pmatrix}
141 \\
109 \\
218 \\
193.7
\end{pmatrix}.
\]

The goal is to solve for \( \mathbf{x} \) using:
1. Gaussian elimination (manual implementation),
2. LU decomposition (Doolittle method, no pivoting),
3. Verification against `numpy.linalg.solve`.

---

## 2. Method 1 — Gaussian Elimination (Forward Elimination + Back Substitution)

### Core Idea
Gaussian elimination transforms the system into an **upper triangular form**:

\[
U \mathbf{x} = \mathbf{c},
\]

which can then be solved by **back substitution**.

### Assumptions
- Pivot elements are non-zero.
- No pivoting is used (numerically fragile but conceptually clear).

---

### Core Code: Gaussian Elimination

```python
import numpy as np

A = np.array([
    [21, 67, 88, 73],
    [76, 63, 70, 20],
    [0, 85, 560, 54],
    [193, 43, 30.2, 29.4]
], dtype=float)

b = np.array([141, 109, 218, 193.7], dtype=float)

n = len(b)

A0 = A.copy()
b0 = b.copy()

# Forward elimination
for k in range(n):
    for i in range(k + 1, n):
        factor = A[i][k] / A[k][k]
        for j in range(k, n):
            A[i][j] -= factor * A[k][j]
        b[i] -= factor * b[k]

# Back substitution
x = np.zeros(n)
for i in range(n - 1, -1, -1):
    total = 0.0
    for j in range(i + 1, n):
        total += A[i][j] * x[j]
    x[i] = (b[i] - total) / A[i][i]

print("x (Gaussian Elimination) =", x)

# Verification
x_true = np.linalg.solve(A0, b0)
print("x (NumPy) =", x_true)
```

---

## 3. Method 2 — LU Decomposition (Doolittle Method)

### Core Idea
Decompose the matrix as:

\[
A = LU,
\]

where:
- \( L \) is a lower triangular matrix with one on the diagonal
- \( U \) is an upper triangular matrix

Then solve:
***forward subtitution***
\[
L \mathbf{y} = \mathbf{b}\]
***back subtitution***
\[
    \quad U \mathbf{x} = \mathbf{y}.
\]

### Core Code: LU Decomposition + Solve

```python
import numpy as np

def lu_decompose_no_pivot(A):
    A = A.astype(float)
    n = A.shape[0]
    L = np.eye(n)
    U = A.copy()

    for k in range(n - 1):
        pivot = U[k, k]
        if abs(pivot) < 1e-12:
            raise ZeroDivisionError("Zero or small pivot encountered.")
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / pivot
            U[i, k:] -= L[i, k] * U[k, k:]
    return L, U

def forward_substitution(L, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
        y[i] /= L[i, i]
    return y

def back_substitution(U, y):
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    return x

# Data
A0 = np.array([
    [21, 67, 88, 73],
    [76, 63, 70, 20],
    [0, 85, 560, 54],
    [193, 43, 30.2, 29.4]
], dtype=float)

b0 = np.array([141, 109, 218, 193.7], dtype=float)

# LU solve
L, U = lu_decompose_no_pivot(A0)
y = forward_substitution(L, b0)
x = back_substitution(U, y)

print("x (LU) =", x)

# Verification
x_np = np.linalg.solve(A0, b0)
print("x (NumPy) =", x_np)

# Residual check
residual = A0 @ x - b0
print("residual =", residual)
print("||residual||_2 =", np.linalg.norm(residual))
```

---

## 4. Method 3 — Compact Gaussian Elimination (Alternative Implementation)

```python
import numpy as np

A = np.array([
    [21, 67, 88, 73],
    [76, 63, 70, 20],
    [0, 85, 560, 54],
    [193, 43, 30.2, 29.4]
], dtype=float)

b = np.array([141, 109, 218, 193.7], dtype=float)

n = len(b)

A0 = A.copy()
b0 = b.copy()

# Forward elimination
for k in range(n - 1):
    pivot = A[k, k]
    if abs(pivot) < 1e-12:
        raise ZeroDivisionError("Zero or small pivot encountered.")
    for i in range(k + 1, n):
        m = A[i, k] / pivot
        for j in range(k, n):
            A[i, j] -= m * A[k, j]
        b[i] -= m * b[k]

# Back substitution
x = np.zeros(n)
for i in range(n - 1, -1, -1):
    s = 0.0
    for j in range(i + 1, n):
        s += A[i, j] * x[j]
    x[i] = (b[i] - s) / A[i, i]

print("x =", x)

# Verification
x_true = np.linalg.solve(A0, b0)
print("x_true =", x_true)
```

---

## 5. Accuracy & Numerical Considerations
- All three methods produce the same solution (within floating-point error).
- Absence of pivoting makes the method:
    -  simpler to understand,
    - but potentially unstable for ill-conditioned matrices.
- Residual norm \[|Ax-b|\] is a practical accuracy check.

---

## 6. When to Use Each Method
- ***Gaussian elimination:***
Best for learning and small systems.

- ***LU decomposition:***
Efficient when solving Ax=b for multiple b.

- ***NumPy solvers:***
Use in real applications: optimized, stable, and well-tested.

---

## 7. Summary
- Linear algebra solvers underpin almost all numerical physics problems.
- Writing solvers manually builds intuition about:
    - pivots,
    - stability,
    - error propagation.
- In practice, understanding how solvers work is more important than reimplementing them.

This block complements earlier topics (ODEs, BVPs, Fourier methods) by focusing on the linear algebra backbone of computational physics.