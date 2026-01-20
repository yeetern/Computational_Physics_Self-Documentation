## 0. Import
```python
import numpy as np
import matplotlib.pyplot as plt
import math
```
## 1. IVP — Euler Method (First-order ODE)

Problem type:
$$
\frac{dy}{dx} = f(x, y), \qquad y(x_0) = y_0
$$

Template:
```python
def f(x, y):
    # CHANGE THIS
    return -x*y   # example

def euler(f, x0, y0, h, x_end):
    x = x0
    y = y0
    xs = [x]
    ys = [y]

    while x < x_end - 1e-12:
        y = y + h * f(x, y)
        x = x + h
        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)

# Example run
xs, ys = euler(f, x0=0, y0=1, h=0.1, x_end=2)
```

---

## 3. BVP — Shooting Method (Euler + Secant)
Problem type:
\[
y'' = g(x, y, y'), 
\qquad y(x_0) = y_0, 
\qquad y(x_f) = y_f
\]


Step 1: Covert to system
```python
def f1(x, y, z):
    return z              # y' = z

def f2(x, y, z):
    # CHANGE THIS (y'')
    return 2*x - x*z + x*y
```

Step 2: Euler Integrator
```python
def euler_system(s, h=0.1):
    x = x0
    y = y0
    z = s

    while x < xf - 1e-12:
        y = y + h * f1(x, y, z)
        z = z + h * f2(x, y, z)
        x = x + h

    return y   # return y(xf)
```

Step 3: Shooting + Secand Method
```python
def F(s):
    return euler_system(s) - yf

def shooting_secant(s1, s2, tol=1e-6):
    for _ in range(50):
        F1 = F(s1)
        F2 = F(s2)
        s3 = s2 - F2*(s2 - s1)/(F2 - F1)
        if abs(F(s3)) < tol:
            return s3
        s1, s2 = s2, s3
    return s2
```

---

## 4. BVP — Finite Difference Method (Central Difference)
Problem type:
\[
y'' + p(x)\,y' + q(x)\,y = r(x)
\]

Grid:
```python
x0, xN = 0.0, 2.0
y0, yN = 1.0, 8.0
h = 0.1

x = np.arange(x0, xN+h/2, h)
N = len(x) - 1
m = N - 1
```

Core Matrix Build:
```python
A = np.zeros((m, m))
b = np.zeros(m)

for i in range(m):
    j = i + 1
    xj = x[j]

    c_jm1 = 1/h**2 - xj/(2*h)
    c_j   = -2/h**2 - xj
    c_jp1 = 1/h**2 + xj/(2*h)
    rhs   = 2*xj   # CHANGE RHS

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
```

Solve:
```python
y_inner = np.linalg.solve(A, b)

y = np.zeros(N+1)
y[0], y[-1] = y0, yN
y[1:-1] = y_inner
```

---

## 5. Linear System — Gaussian Elimination (No Pivot)

```python
def gaussian_elimination(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)

    for k in range(n):
        for i in range(k+1, n):
            factor = A[i,k]/A[k,k]
            A[i,k:] -= factor*A[k,k:]
            b[i] -= factor*b[k]

    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i,i+1:], x[i+1:]))/A[i,i]

    return x
```

---

## 6. Linear System — LU Decomposition (Doolittle)
```python
def lu_decompose(A):
    n = A.shape[0]
    L = np.eye(n)
    U = A.copy()

    for k in range(n-1):
        for i in range(k+1, n):
            L[i,k] = U[i,k]/U[k,k]
            U[i,k:] -= L[i,k]*U[k,k:]

    return L, U
```

```python
def forward_sub(L, b):
    y = np.zeros(len(b))
    for i in range(len(b)):
        y[i] = b[i] - np.dot(L[i,:i], y[:i])
    return y

def back_sub(U, y):
    x = np.zeros(len(y))
    for i in range(len(y)-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i,i+1:], x[i+1:]))/U[i,i]
    return x
```

---

## 7. Fourier — Manual DFT / IDFT
```python
def dft(x):
    x = np.asarray(x, dtype=complex)
    N = len(x)
    X = np.zeros(N, dtype=complex)

    for k in range(N):
        for n in range(N):
            X[k] += x[n]*np.exp(-2j*np.pi*k*n/N)
    return X

def idft(X):
    N = len(X)
    x = np.zeros(N, dtype=complex)
    for n in range(N):
        for k in range(N):
            x[n] += X[k]*np.exp(2j*np.pi*k*n/N)
        x[n] /= N
    return x
```

---

## 8. Fourier — FFT
```python
X = np.fft.fft(signal)
freq = np.fft.fftfreq(len(signal), d=dt)
signal_back = np.fft.ifft(X).real
```

---

## 9. Frequency Filtering (Band-Pass)
```python
def bandpass(X, freq, f0, width):
    Xf = np.zeros_like(X)
    mask = np.abs(freq - f0) < width
    mask |= np.abs(freq + f0) < width
    Xf[mask] = X[mask]
    return Xf
```

---

## 10. Plot Template
```python
plt.plot(x, y, 'o-')
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()
```

---

## Exam Strategy
- ODE? → Euler / RK4
- Two boundary values? → Shooting or FDM
- Matrix given? → Gaussian or LU
- Signal + noise? → DFT → filter → IDFT