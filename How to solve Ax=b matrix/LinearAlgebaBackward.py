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

# Step 1: make zeros below diagonal
for k in range(n):
    for i in range(k+1, n):
        factor = A[i][k] / A[k][k]
        for j in range(k, n):
            A[i][j] -= factor * A[k][j]
        b[i] -= factor * b[k]

# Step 2: back substitution
x = np.zeros(n)
for i in range(n-1, -1, -1):
    total = 0
    for j in range(i+1, n):
        total += A[i][j] * x[j]
    x[i] = (b[i] - total) / A[i][i]

print(x)

x_true = np.linalg.solve(A0, b0)
print (x_true)