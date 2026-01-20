How to solve linear algebra: A*x = b?

Methods:
1️⃣ Gaussian Elimination (Forward + Backward)
# Forward elimination
for k in range(n):
    for i in range(k+1, n):
        factor = A[i][k] / A[k][k]
        for j in range(k, n):
            A[i][j] -= factor * A[k][j]
        b[i] -= factor * b[k]

# Back substitution
for i in range(n-1, -1, -1):
    s = 0
    for j in range(i+1, n):
        s += A[i][j] * x[j]
    x[i] = (b[i] - s) / A[i][i]
------------------------------------------------------------
2️⃣ LU Decomposition (Doolittle: A = L·U)
for k in range(n):
    # U-row
    for j in range(k, n):
        U[k][j] = A[k][j] - sum(L[k][p] * U[p][j] for p in range(k))

    # L-column
    for i in range(k+1, n):
        L[i][k] = (A[i][k] - sum(L[i][p] * U[p][k] for p in range(k))) / U[k][k]
------------------------------------------------------------
