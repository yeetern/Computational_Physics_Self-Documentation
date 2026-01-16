import numpy as np
import math


# ------------------------------------------------
# Crout LU decomposition + forward/back substitution
# ------------------------------------------------
def crout_lu(A: np.ndarray):
    A = A.astype(float)
    n = A.shape[0]
    L = np.zeros((n, n), dtype=float)
    U = np.zeros((n, n), dtype=float)

    # Crout: diag(U) = 1
    for i in range(n):
        U[i, i] = 1.0

    for j in range(n):
        # Build column j of L
        for i in range(j, n):
            s = 0.0
            for k in range(j):
                s += L[i, k] * U[k, j]
            L[i, j] = A[i, j] - s

        if abs(L[j, j]) < 1e-14:
            raise ZeroDivisionError(f"Zero pivot at L[{j},{j}] = {L[j,j]}")

        # Build row j of U (right of diagonal)
        for i in range(j + 1, n):
            s = 0.0
            for k in range(j):
                s += L[j, k] * U[k, i]
            U[j, i] = (A[j, i] - s) / L[j, j]

    return L, U


def forward_substitution(L: np.ndarray, b: np.ndarray):
    n = L.shape[0]
    y = np.zeros(n, dtype=float)
    for i in range(n):
        s = 0.0
        for k in range(i):
            s += L[i, k] * y[k]
        y[i] = (b[i] - s) / L[i, i]
    return y


def back_substitution(U: np.ndarray, y: np.ndarray):
    n = U.shape[0]
    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        s = 0.0
        for k in range(i + 1, n):
            s += U[i, k] * x[k]
        x[i] = (y[i] - s) / U[i, i]
    return x


# ------------------------------------------------
# Build A from Laplace/Poisson stencil (2×2 interior)
# and build b from -h² f(x_i,y_j) (Dirichlet boundaries are zero)
# ------------------------------------------------
def f_source(x, y):
    return -2.0 * math.pi**2 * math.sin(math.pi * x) * math.sin(math.pi * y)


def assemble_poisson_Ab(m, n, a=0.0, b=1.0, c=0.0, d=1.0):
    """
    Assemble A x = rhs for Poisson on [a,b]×[c,d] with m×n interior nodes.
    Here boundaries are zero so only source term contributes to RHS.
    """
    hx = (b - a) / (m + 1)
    hy = (d - c) / (n + 1)

    if abs(hx - hy) > 1e-14:
        raise ValueError("This implementation assumes square grid hx=hy (as in the question).")

    h = hx
    N = m * n
    A = np.zeros((N, N), dtype=float)
    rhs = np.zeros(N, dtype=float)

    def idx(i, j):
        # i=1..m, j=1..n
        return (j - 1) * m + (i - 1)

    for j in range(1, n + 1):
        yj = c + j * h
        for i in range(1, m + 1):
            xi = a + i * h
            p = idx(i, j)

            # Center coefficient
            A[p, p] = 4.0

            # Left neighbor
            if i - 1 >= 1:
                A[p, idx(i - 1, j)] = -1.0
            # else boundary is 0 -> no addition to rhs

            # Right neighbor
            if i + 1 <= m:
                A[p, idx(i + 1, j)] = -1.0

            # Bottom neighbor
            if j - 1 >= 1:
                A[p, idx(i, j - 1)] = -1.0

            # Top neighbor
            if j + 1 <= n:
                A[p, idx(i, j + 1)] = -1.0

            # Poisson forcing on RHS: 4u - neighbors = -h^2 f
            rhs[p] = - (h**2) * f_source(xi, yj)

    return A, rhs, h


# ------------------------------------------------
# Main
# ------------------------------------------------
if __name__ == "__main__":
    # 2×2 interior grid (as required)
    m, n = 2, 2

    # Assemble system
    A, rhs, h = assemble_poisson_Ab(m, n)

    # Solve using Crout LU
    L, U = crout_lu(A)
    y = forward_substitution(L, rhs)
    x = back_substitution(U, y)

    # Extract interior values
    u11, u21, u12, u22 = x

    np.set_printoptions(precision=10, suppress=True)

    print("\nQuestion 3(c): Poisson 2×2 interior (Crout LU, no linalg.solve)\n")
    print(f"Grid spacing h = {h:.6f}\n")
    print("A =\n", A)
    print("\nRHS =\n", rhs)

    print("\nInterior solution u (approx):")
    print(f"u11 = {u11:.10f}")
    print(f"u21 = {u21:.10f}")
    print(f"u12 = {u12:.10f}")
    print(f"u22 = {u22:.10f}")