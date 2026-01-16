import numpy as np

# Liebmann (Gauss–Seidel) Iteration with Over-Relaxation (SOR)
# for 2D Laplace Equation

# Boundary Conditions (°C)
T_left   = 50.0
T_right  = 25.0
T_bottom = 0.0
T_top    = 75.0

# Interior grid size (same system as Part a)
m, n = 2, 2

# Over-relaxation parameter and tolerance
lam = 1.5          # 1 ≤ λ ≤ 2
tol = 1e-6
max_iter = 10000

# Grid including boundaries
# Size: (n+2) × (m+2)
u = np.zeros((n+2, m+2))

# Apply boundary conditions
u[:, 0]  = T_left
u[:, -1] = T_right
u[0, :]  = T_bottom
u[-1, :] = T_top

# Initial guess: average of boundaries
u[1:-1, 1:-1] = (T_left + T_right + T_bottom + T_top) / 4

# Liebmann Iteration (Gauss–Seidel + SOR)
for k in range(1, max_iter + 1):
    max_diff = 0.0

    for j in range(1, n + 1):
        for i in range(1, m + 1):

            u_star = 0.25 * (
                u[j, i+1] + u[j, i-1] +
                u[j+1, i] + u[j-1, i]
            )

            u_new = lam * u_star + (1 - lam) * u[j, i]
            diff = abs(u_new - u[j, i])

            u[j, i] = u_new
            max_diff = max(max_diff, diff)

    if max_diff < tol:
        print(f"Converged in {k} iterations.")
        break

# Extract interior values
T11 = u[1, 1]
T21 = u[1, 2]
T12 = u[2, 1]
T22 = u[2, 2]

print("\n(c) Liebmann Iteration with Over-Relaxation\n")
print(f"T11 = {T11:.6f}")
print(f"T21 = {T21:.6f}")
print(f"T12 = {T12:.6f}")
print(f"T22 = {T22:.6f}")
