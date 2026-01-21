#Alternative Assessment 1 Question 1
#Program Name: Finite Central Difference for BVP
#Subject: SIF3012 Computational Physics
#Author: Tan Yee Tern
#Student ID: 23006131
#Email: 23006131@siswa.um.edu.my
#Date of Creation: Tuesday Jan 20

#--------------------------------------------------------------------------------------------

import numpy as np

# As the question give:
# Parameters
L = 10.0
h = 2.0
alpha = 0.01
T_alp = 20.0
T0 = 40.0
TL = 200.0

# Define function
# Central Difference
def build_matrix(L, h, alpha, T_alp, T0, TL):
    x = np.arange(0, L + h, h)
    n = len(x) - 2  # interior nodes

    ah2 = alpha * h**2
    A = np.zeros((n, n))
    b = np.ones(n) * ah2 * T_alp

    for i in range(n):
        A[i, i] = 2 + ah2
        if i > 0:
            A[i, i-1] = -1
        if i < n-1:
            A[i, i+1] = -1

    b[0] += T0
    b[-1] += TL

    return x, A, b

# LU decomposition
def lu_decomposition(A):
    n = A.shape[0]
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        L[i, i] = 1

    for k in range(n):
        for j in range(k, n):
            U[k, j] = A[k, j] - np.dot(L[k, :k], U[:k, j])
        for i in range(k+1, n):
            L[i, k] = (A[i, k] - np.dot(L[i, :k], U[:k, k])) / U[k, k]

    return L, U


def forward_sub(L, b):
    y = np.zeros(len(b))
    for i in range(len(b)):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    return y


def backward_sub(U, y):
    x = np.zeros(len(y))
    for i in range(len(y)-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    return x

x, A, b = build_matrix(L, h, alpha, T_alp, T0, TL)

Lmat, Umat = lu_decomposition(A)
y = forward_sub(Lmat, b)
Tint = backward_sub(Umat, y)

# Full temperature vector
T = np.zeros(len(x))
T[0] = T0
T[-1] = TL
T[1:-1] = Tint

# Output
for xi, Ti in zip(x, T):
    print(f"x = {xi:>4.1f} m,  T = {Ti:>8.3f} °C")