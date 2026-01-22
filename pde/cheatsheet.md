# SIF3012 — Chapter 4: Partial Differential Equations (PDEs)
## Final Exam Cheat Sheet

---

## 1. What Questions Usually Ask

Typical PDE questions require you to:

1. **Classify a PDE** (elliptic / parabolic / hyperbolic)
2. **Write down the governing equation**
3. **Discretize using finite difference**
4. **State stability conditions**
5. **Explain physical meaning**
6. **Discuss boundary and initial conditions**
7. **Distinguish steady vs non-steady state**
8. **Comment on numerical accuracy / stability**

---

## 2. Classification of Second-Order PDEs (Must Memorize)

General form:
\[
A u_{xx} + B u_{xy} + C u_{yy} + \cdots = 0
\]

Discriminant:
\[
\Delta = B^2 - 4AC
\]

| Type | Condition | Physical Meaning |
|----|----|----|
| Elliptic | \( \Delta < 0 \) | Steady-state, equilibrium |
| Parabolic | \( \Delta = 0 \) | Diffusion / relaxation |
| Hyperbolic | \( \Delta > 0 \) | Wave propagation |

---

## 3. Elliptic PDE — Laplace / Poisson Equation

### Governing Equation
Laplace:
\[
\nabla^2 u = 0
\]

Poisson:
\[
\nabla^2 u = f(x,y)
\]

---

### Physical Meaning
- **Steady-state system**
- No time dependence
- Examples:
  - Electrostatics
  - Steady heat conduction
  - Potential flow

---

### Finite Difference (2D Laplace)
\[
u_{i,j} = \frac{1}{4}
\left(
u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1}
\right)
\]

---

### Key Exam Points
- Leads to **linear system**
- Requires **iterative solvers**
- Boundary conditions determine uniqueness
- No stability condition (no time)

---

## 4. Parabolic PDE — Diffusion / Heat Equation

### Governing Equation
\[
\frac{\partial u}{\partial t}
=
D \frac{\partial^2 u}{\partial x^2}
\]

---

### Physical Meaning
- Time-dependent relaxation
- Smoothing of gradients
- Examples:
  - Heat diffusion
  - Particle diffusion

---

### Explicit Finite Difference Scheme

\[
u_i^{n+1}=
u_i^n
+
r \left(
u_{i+1}^n - 2u_i^n + u_{i-1}^n
\right)
\]

where:
\[
r = \frac{D \Delta t}{(\Delta x)^2}
\]

---

### Stability Condition (Must State)
\[
\boxed{r \le \frac{1}{2}}
\]

If violated → solution blows up.

---

### Steady vs Non-Steady State
- **Non-steady**: solution changes with time
- **Steady**: \( \partial u / \partial t = 0 \Rightarrow \) reduces to Laplace equation

---

## 5. Hyperbolic PDE — Wave Equation

### Governing Equation
\[
\frac{\partial^2 u}{\partial t^2}=
c^2 \frac{\partial^2 u}{\partial x^2}
\]

---

### Physical Meaning
- Wave propagation
- Information travels with finite speed \(c\)
- Examples:
  - Vibrating string
  - Sound waves

---

### Finite Difference Scheme (Central)
\[
u_i^{n+1}=
2u_i^n - u_i^{n-1}
+
\lambda^2
\left(
u_{i+1}^n - 2u_i^n + u_{i-1}^n
\right)
\]

where:
\[
\lambda = \frac{c \Delta t}{\Delta x}
\]

---

### Stability Condition (Courant Condition)
\[
\boxed{\lambda < 1}
\]

---

## 6. Boundary & Initial Conditions (Very Important)

### Initial Conditions
- Required for **time-dependent PDEs**
- Examples:
  - Initial temperature
  - Initial displacement
  - Initial velocity

---

### Boundary Conditions
- **Dirichlet**: value specified
  \[
  u = \text{constant}
  \]
- **Neumann**: derivative specified
  \[
  \frac{\partial u}{\partial x} = 0
  \]
- **Periodic**: wrap-around boundaries

---

## 7. Numerical Accuracy & Stability (Conceptual)

### Accuracy
- Determined by:
  - Grid spacing \( \Delta x \)
  - Time step \( \Delta t \)
  - Order of finite difference

---

### Stability
- Diffusion: controlled by \( r \)
- Wave equation: controlled by Courant number
- Instability → exponential growth of error

---

## 8. Common Exam Comments (Memorize These)

### Why Finite Difference?
- Converts PDE → algebraic equations
- Simple and intuitive
- Easy to implement

---

### Limitations
- Stability restrictions on \( \Delta t \)
- Numerical diffusion / dispersion
- Computational cost for fine grids
- Boundary handling is critical

---

### Improvements
- Implicit schemes (unconditionally stable)
- Crank–Nicolson
- Higher-order stencils
- Adaptive mesh refinement

---

## 9. One-Sentence Killer Summary (Exam Gold)

> Partial differential equations describe space- and time-dependent physical systems, and their numerical solutions using finite difference methods require careful treatment of discretization, boundary conditions, and stability to obtain physically meaningful results.

---

## Appendix: Explicit Finite Difference Code (Diffusion Equation)

```python
import numpy as np
import matplotlib.pyplot as plt

# Physical parameters
D = 1.0                 # diffusion coefficient
L = 1.0                 # length of domain
T = 0.1                 # total simulation time

# Numerical parameters
Nx = 51                 # number of spatial grid points
Nt = 500                # number of time steps
dx = L / (Nx - 1)
dt = T / Nt

# Stability parameter (must satisfy r <= 0.5)
r = D * dt / dx**2

# Spatial grid
x = np.linspace(0, L, Nx)

# Initial condition: localized peak
u = np.exp(-100 * (x - 0.5)**2)

# Time evolution (explicit scheme)
for n in range(Nt):
    u_new = u.copy()    # use a copy to avoid overwriting
    for i in range(1, Nx - 1):
        u_new[i] = (
            u[i]
            + r * (u[i+1] - 2*u[i] + u[i-1])
        )
    u = u_new

# Plot final result
plt.plot(x, u)
plt.xlabel("x")
plt.ylabel("u(x,t)")
plt.title("1D Diffusion Equation (Explicit Finite Difference)")
plt.show()
```

---

## Appendix: Steady vs Non-Steady State Plot (Using Pandas)

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data (example: time vs temperature)
# Replace filename and column names according to your dataset
data = pd.read_csv("steady_vs_nonsteady.csv")

# Assume columns:
# time, steady_state, nonsteady_state
t = data["time"]
u_steady = data["steady_state"]
u_nonsteady = data["nonsteady_state"]

# Plot
plt.plot(t, u_steady, label="Steady State", linestyle="--")
plt.plot(t, u_nonsteady, label="Non-Steady State")

plt.xlabel("Time")
plt.ylabel("u")
plt.title("Steady vs Non-Steady State")
plt.legend()
plt.grid(True)
plt.show()
```

---

## Appendix: Wave Equation (Explicit Finite Difference Scheme)

```python
import numpy as np
import matplotlib.pyplot as plt

# Physical parameters
c = 1.0                 # wave speed
L = 1.0                 # length of string
T = 1.0                 # total simulation time

# Numerical parameters
Nx = 101                # number of spatial grid points
Nt = 500                # number of time steps
dx = L / (Nx - 1)
dt = T / Nt

# Courant number (must satisfy c*dt/dx < 1)
lam = c * dt / dx

# Spatial grid
x = np.linspace(0, L, Nx)

# Initial conditions
u_prev = np.zeros(Nx)                   # u(x, t-dt)
u = np.exp(-100 * (x - 0.5)**2)          # initial displacement
u_next = np.zeros(Nx)                   # u(x, t+dt)

# Time evolution (central difference in time and space)
for n in range(Nt):
    for i in range(1, Nx - 1):
        u_next[i] = (
            2*u[i] - u_prev[i]
            + lam**2 * (u[i+1] - 2*u[i] + u[i-1])
        )

    # Update time levels
    u_prev = u.copy()
    u = u_next.copy()

# Plot final displacement
plt.plot(x, u)
plt.xlabel("x")
plt.ylabel("u(x,t)")
plt.title("1D Wave Equation (Explicit Finite Difference)")
plt.show()
```

---

## Appendix: Laplace Equation (Steady-State Solver — Gauss–Seidel)

```python
import numpy as np
import matplotlib.pyplot as plt

# Grid parameters
Nx, Ny = 50, 50
Lx, Ly = 1.0, 1.0
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)

# Initialize solution array
u = np.zeros((Ny, Nx))

# Boundary conditions (Dirichlet)
u[0, :] = 1.0        # bottom boundary
u[-1, :] = 0.0       # top boundary
u[:, 0] = 0.0        # left boundary
u[:, -1] = 0.0       # right boundary

# Iteration parameters
max_iter = 5000
tol = 1e-6

# Gauss–Seidel iteration
for it in range(max_iter):
    u_old = u.copy()

    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            u[j, i] = 0.25 * (
                u[j, i+1] + u[j, i-1]
                + u[j+1, i] + u[j-1, i]
            )

    # Convergence check
    if np.max(np.abs(u - u_old)) < tol:
        print(f"Converged after {it} iterations")
        break

# Plot steady-state solution
plt.imshow(u, origin="lower", extent=[0, Lx, 0, Ly], cmap="inferno")
plt.colorbar(label="u")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Laplace Equation (Steady-State Solution)")
plt.show()
```

---

## Appendix: Poisson Equation (Steady-State Solver — Gauss–Seidel)

```python
import numpy as np
import matplotlib.pyplot as plt

# Grid parameters
Nx, Ny = 50, 50
Lx, Ly = 1.0, 1.0
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)

# Source term f(x, y)
f = np.ones((Ny, Nx)) * 50.0

# Initialize solution array
u = np.zeros((Ny, Nx))

# Boundary conditions (Dirichlet: u = 0)
u[0, :] = 0.0
u[-1, :] = 0.0
u[:, 0] = 0.0
u[:, -1] = 0.0

# Iteration parameters
max_iter = 5000
tol = 1e-6

# Gauss–Seidel iteration for Poisson equation
for it in range(max_iter):
    u_old = u.copy()

    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            u[j, i] = 0.25 * (
                u[j, i+1] + u[j, i-1]
                + u[j+1, i] + u[j-1, i]
                - dx**2 * f[j, i]
            )

    # Convergence check
    if np.max(np.abs(u - u_old)) < tol:
        print(f"Converged after {it} iterations")
        break

# Plot steady-state solution
plt.imshow(u, origin="lower", extent=[0, Lx, 0, Ly], cmap="viridis")
plt.colorbar(label="u")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Poisson Equation (Steady-State Solution)")
plt.show()
```

---

## Appendix: Laplace / Poisson Equation (SOR — Faster Convergence)

```python
import numpy as np
import matplotlib.pyplot as plt

# Grid parameters
Nx, Ny = 50, 50
Lx, Ly = 1.0, 1.0
dx = Lx / (Nx - 1)

# Choose equation type:
# - For Laplace: set f = 0 everywhere
# - For Poisson: set a nonzero source term
f = np.zeros((Ny, Nx))          # Laplace example (change to nonzero for Poisson)
# f[:] = 50.0                   # Uncomment for Poisson example

# Initialize solution array
u = np.zeros((Ny, Nx))

# Boundary conditions (Dirichlet example)
u[0, :] = 1.0        # bottom boundary
u[-1, :] = 0.0       # top boundary
u[:, 0] = 0.0        # left boundary
u[:, -1] = 0.0       # right boundary

# SOR parameters
omega = 1.7          # relaxation factor (1 < omega < 2 usually speeds up)
max_iter = 5000
tol = 1e-6

for it in range(max_iter):
    u_old = u.copy()

    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            # Gauss–Seidel "target" value
            u_gs = 0.25 * (
                u[j, i+1] + u[j, i-1]
                + u[j+1, i] + u[j-1, i]
                - dx**2 * f[j, i]
            )

            # SOR update
            u[j, i] = u[j, i] + omega * (u_gs - u[j, i])

    # Convergence check
    if np.max(np.abs(u - u_old)) < tol:
        print(f"Converged after {it} iterations (omega = {omega})")
        break

# Plot solution
plt.imshow(u, origin="lower", extent=[0, Lx, 0, Ly], cmap="plasma")
plt.colorbar(label="u")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Elliptic PDE Solver (SOR)")
plt.show()
```

---

## Appendix: 2D Diffusion Equation (Explicit Scheme + Animation)

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Grid parameters
nx, ny = 100, 100
T = 400                    # number of frames / time steps

# Initialize temperature field
u = np.zeros((nx, ny))

# Initial hot spot (you can change these)
u[30, 20] = 1.0

# Stability-like factor for this demo code (effective r = 1/4 here)
r = 1/4

fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title("2D Diffusion (Explicit Update)")
plot = ax.contourf(u, cmap="jet")
ax.set_xlabel("x index")
ax.set_ylabel("y index")

def update(frame):
    global u, plot

    # copy old state so updates use only previous time level
    u_new = u.copy()

    # update interior points only
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            u_new[i, j] = (
                u[i, j]
                + r * (
                    u[i+1, j] + u[i-1, j]
                    + u[i, j+1] + u[i, j-1]
                    - 4*u[i, j]
                )
            )

    u[:] = u_new

    # redraw contour plot
    for c in plot.collections:
        c.remove()
    plot = ax.contourf(u, cmap="jet")
    return plot

anim = animation.FuncAnimation(fig, update, frames=T, interval=30)
plt.show()
```

---

## Appendix: Wave Equation — Boundary Conditions (Correct Implementation)

This appendix demonstrates how different boundary conditions are implemented
for the 1D wave equation using an explicit finite difference scheme.

Boundary conditions included:
- Dirichlet (fixed ends)
- Neumann (free ends)
- Periodic (wrap-around, implemented via modulo indexing)

---

### Governing Equation

\[
\frac{\partial^2 u}{\partial t^2}=
c^2 \frac{\partial^2 u}{\partial x^2}
\]

---

### Code Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Physical and numerical parameters
# -----------------------------
c = 1.0
L = 1.0
T = 1.0

Nx = 201
Nt = 1200
dx = L / (Nx - 1)
dt = T / Nt
lam = c * dt / dx    # Courant number (must be < 1)

# Choose boundary condition:
# "dirichlet", "neumann", or "periodic"
bc_type = "dirichlet"

# Spatial grid
x = np.linspace(0, L, Nx)

# -----------------------------
# Initial conditions
# -----------------------------
u_prev = np.zeros(Nx)                 # u at time n-1
u = np.exp(-200 * (x - 0.3)**2)        # u at time n
u_next = np.zeros(Nx)                 # u at time n+1

# -----------------------------
# Time stepping
# -----------------------------
for n in range(Nt):

    if bc_type == "periodic":
        # Periodic boundary via modulo indexing
        for i in range(Nx):
            ip = (i + 1) % Nx
            im = (i - 1) % Nx
            u_next[i] = (
                2*u[i] - u_prev[i]
                + lam**2 * (u[ip] - 2*u[i] + u[im])
            )

    else:
        # Interior points
        for i in range(1, Nx - 1):
            u_next[i] = (
                2*u[i] - u_prev[i]
                + lam**2 * (u[i+1] - 2*u[i] + u[i-1])
            )

        if bc_type == "dirichlet":
            # Fixed ends
            u_next[0] = 0.0
            u_next[-1] = 0.0

        elif bc_type == "neumann":
            # Zero spatial derivative at boundaries
            u_next[0] = u_next[1]
            u_next[-1] = u_next[-2]

        else:
            raise ValueError("bc_type must be 'dirichlet', 'neumann', or 'periodic'.")

    # Shift time levels
    u_prev, u = u, u_next
    u_next = np.zeros(Nx)

# -----------------------------
# Plot final state
# -----------------------------
plt.plot(x, u)
plt.xlabel("x")
plt.ylabel("u(x,t)")
plt.title(f"1D Wave Equation (BC = {bc_type})")
plt.show()
