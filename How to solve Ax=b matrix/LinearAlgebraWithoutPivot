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

# Forward elimination: A -> U, b -> c
for k in range(n - 1):
    pivot = A[k, k]
    if abs(pivot) < 1e-12:
        raise ZeroDivisionError(f"Zero/small pivot at k={k}. Consider pivoting.")
    for i in range(k + 1, n):
        m = A[i, k] / pivot
        for j in range(k, n):
            A[i, j] = A[i, j] - m * A[k, j]
        b[i] = b[i] - m * b[k]

# Back substitution: Ux = c
x = np.zeros(n)
for i in range(n - 1, -1, -1):
    s = 0.0
    for j in range(i + 1, n):
        s += A[i, j] * x[j]
    x[i] = (b[i] - s) / A[i, i]

print("x =", x)

x_true = np.linalg.solve(A0, b0)
print("x_true =", x_true)