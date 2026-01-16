import numpy as np

# Crout LU decomposition + forward/back substitution

def crout_lu(A: np.ndarray):
    A = A.astype(float)
    n = A.shape[0]
    L = np.zeros((n, n), dtype=float)
    U = np.zeros((n, n), dtype=float)

    for i in range(n):
        U[i, i] = 1.0

    for j in range(n):
        for i in range(j, n):
            s = 0.0
            for k in range(j):
                s += L[i, k] * U[k, j]
            L[i, j] = A[i, j] - s

        if abs(L[j, j]) < 1e-14:
            raise ZeroDivisionError(f"Zero pivot at L[{j},{j}] = {L[j,j]}")

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

# Build A and b from the equation (5-point stencil)
def assemble_laplace_Ab(m, n, T_left, T_right, T_bottom, T_top):
    """
    Assemble A x = b for Laplace equation on a unit square
    using a 5-point stencil on an m×n interior grid.

    Unknowns are interior nodes (i=1..m, j=1..n).
    We map (i,j) -> p index by: p = (j-1)*m + (i-1)
    """

    N = m * n
    A = np.zeros((N, N), dtype=float)
    b = np.zeros(N, dtype=float)

    def idx(i, j):
        """Map interior (i,j) to 1D index p."""
        return (j - 1) * m + (i - 1)

    # Loop over each interior node (i,j)
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            p = idx(i, j)

            # Center coefficient from 4u_ij - neighbors = boundary terms
            A[p, p] = 4.0

            # Left neighbor (i-1, j)
            if i - 1 >= 1:  # interior neighbor
                A[p, idx(i - 1, j)] = -1.0
            else:           # boundary x=0
                b[p] += T_left

            # Right neighbor (i+1, j)
            if i + 1 <= m:
                A[p, idx(i + 1, j)] = -1.0
            else:           # boundary x=1
                b[p] += T_right

            # Bottom neighbor (i, j-1)
            if j - 1 >= 1:
                A[p, idx(i, j - 1)] = -1.0
            else:           # boundary y=0
                b[p] += T_bottom

            # Top neighbor (i, j+1)
            if j + 1 <= n:
                A[p, idx(i, j + 1)] = -1.0
            else:           # boundary y=1
                b[p] += T_top

    return A, b

# Main: boundary values + solve with LU
if __name__ == "__main__":
    # Boundary Conditions (°C)
    T_left   = 50.0
    T_right  = 25.0
    T_bottom = 0.0
    T_top    = 75.0

    # 2×2 interior grid (same as Part (a))
    m, n = 2, 2

    # Assemble A and b from the Laplace equation (no manual A)
    A, b = assemble_laplace_Ab(m, n, T_left, T_right, T_bottom, T_top)

    # Solve using Crout LU
    L, U = crout_lu(A)
    y = forward_substitution(L, b)
    x = back_substitution(U, y)

    # x ordering corresponds to (i,j) in the mapping:
    # p=0:(1,1)=T11, p=1:(2,1)=T21, p=2:(1,2)=T12, p=3:(2,2)=T22
    T11, T21, T12, T22 = x

    np.set_printoptions(precision=6, suppress=True)

    print("\n(b) LU (Crout) Solver Output (A built from equation)\n")
    print("A =\n", A)
    print("\nb = ", b)

    print("\nInterior temperatures (°C):")
    print(f"T11 = {T11:.6f}")
    print(f"T21 = {T21:.6f}")
    print(f"T12 = {T12:.6f}")
    print(f"T22 = {T22:.6f}")
