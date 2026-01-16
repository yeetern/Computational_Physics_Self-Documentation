import numpy as np

def lu_decompose_no_pivot(A):
    """
    Doolittle LU decomposition (no pivoting):
    A = L U, where L has 1s on diagonal.
    Assumes all pivots U[k,k] != 0.
    """
    A = A.astype(float)
    n = A.shape[0]

    L = np.eye(n)
    U = A.copy()

    for k in range(n - 1):
        pivot = U[k, k]
        if abs(pivot) < 1e-12:
            raise ZeroDivisionError(f"Small/zero pivot at k={k}: {pivot}. Consider pivoting.")

        for i in range(k + 1, n):
            L[i, k] = U[i, k] / pivot          # multiplier
            U[i, k:] -= L[i, k] * U[k, k:]     # eliminate entries below pivot

    return L, U

def forward_substitution(L, b):
    """Solve L y = b where L is lower triangular (assume diag nonzero, here diag=1)."""
    n = len(b)
    y = np.zeros(n, dtype=float)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
        y[i] /= L[i, i]
    return y

def back_substitution(U, y):
    """Solve U x = y where U is upper triangular."""
    n = len(y)
    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        if abs(U[i, i]) < 1e-12:
            raise ZeroDivisionError(f"Zero pivot at i={i}: {U[i,i]}")
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    return x

# --- your data ---
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

print("L=\n", L)
print("U=\n", U)
print("x (LU) =", x)

# Check against numpy (important: use original A0, b0)
x_np = np.linalg.solve(A0, b0)
print("x (numpy) =", x_np)

# Residual check
res = A0 @ x - b0
print("residual =", res)
print("||residual||_2 =", np.linalg.norm(res))
