import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import dblquad

# 1) Define Integrand
# f_A(x, y) = cos(pi x/2) * cos(pi y/2)
# Domain: (x, y) in [0,1] x [0,1]
def f(x, y):
    return np.cos(0.5 * np.pi * x) * np.cos(0.5 * np.pi * y)

# Limits on the unit square
x_min, x_max = 0.0, 1.0
y_min, y_max = 0.0, 1.0

# "Exact" calculation using SciPy dblquad
exact_result, exact_err_est = dblquad(
    lambda y, x: f(x, y),
    x_min, x_max,
    lambda x: y_min,
    lambda x: y_max
)

# 2) Monte Carlo Integration
N = 10000  # Number of random samples

rng = np.random.default_rng(seed=12345) # For reproducible

# Random points in the domain
x_samples = rng.uniform(low=x_min, high=x_max, size=N)
y_samples = rng.uniform(low=y_min, high=y_max, size=N)

# Function values
z_values = f(x_samples, y_samples)

# Area of the domain
domain_area = (x_max - x_min) * (y_max - y_min)

# Monte Carlo estimate of integral
monte_carlo_result = z_values.mean() * domain_area

# Correct Monte Carlo standard error:
# SE(I) = area * std(f) / sqrt(N)
monte_carlo_error = domain_area * np.std(z_values, ddof=1) / np.sqrt(N)

# Print results
print(f"--- Results (Group A) ---")
print(f"Exact Result (dblquad):      {exact_result:.8f}  (quad err est ~ {exact_err_est:.2e})")
print(f"Analytic Result (4/pi^2):    {analytic_result:.8f}")
print(f"Monte Carlo Result:          {monte_carlo_result:.8f} ± {monte_carlo_error:.8f} (1σ)")
print(f"Absolute error vs dblquad:   {abs(monte_carlo_result - exact_result):.8f}")

# Grid for smooth surface plot
x_grid = np.linspace(x_min, x_max, 80)
y_grid = np.linspace(y_min, y_max, 80)
X, Y = np.meshgrid(x_grid, y_grid)
Z = f(X, Y)

# Setup figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.85)

# Add result text on plot (2D overlay)
result_text = (
    f"Exact (dblquad): {exact_result:.6f}\n"
    f"Analytic 4/pi^2: {analytic_result:.6f}\n"
    f"MC (N={N}): {monte_carlo_result:.6f} ± {monte_carlo_error:.6f}"
)
ax.text2D(
    0.05, 0.95, result_text,
    transform=ax.transAxes, fontsize=12,
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.85)
)

# Labels
ax.set_title(r'Group A: $f(x,y)=\cos(\pi x/2)\cos(\pi y/2)$ on $[0,1]^2$')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x,y)')

# Colorbar
fig.colorbar(surf, shrink=0.55, aspect=12, label='f(x, y)')

# Save image
plt.savefig('GroupA_MonteCarlo_double_integral.png', dpi=200, bbox_inches='tight')
plt.show()

# Optional Convergence study
"""
do_convergence_study = True

if do_convergence_study:
    Ns = np.unique(np.logspace(2, 6, 14).astype(int))  # 1e2 ... 1e6
    estimates = []
    errors = []
    abs_errors = []

    # Use a fresh RNG stream for convergence study (still reproducible)
    rng2 = np.random.default_rng(seed=2026)

    for n in Ns:
        xs = rng2.uniform(x_min, x_max, size=n)
        ys = rng2.uniform(y_min, y_max, size=n)
        vals = f(xs, ys)

        I_hat = domain_area * np.mean(vals)
        dI = domain_area * np.std(vals, ddof=1) / np.sqrt(n)

        estimates.append(I_hat)
        errors.append(dI)
        abs_errors.append(abs(I_hat - analytic_result))

    estimates = np.array(estimates)
    errors = np.array(errors)
    abs_errors = np.array(abs_errors)

    # Plot estimate vs N with error bars
    plt.figure(figsize=(8, 5))
    plt.errorbar(Ns, estimates, yerr=errors, fmt='o', capsize=3, label='MC estimate ±1σ')
    plt.axhline(analytic_result, linestyle='--', label='Analytic 4/π²')
    plt.xscale('log')
    plt.xlabel('Number of samples N (log scale)')
    plt.ylabel('Integral estimate')
    plt.title('Convergence of MC estimate (Group A)')
    plt.grid(True, which='both', linestyle=':')
    plt.legend()
    plt.tight_layout()
    plt.savefig('GroupA_MC_convergence_estimate.png', dpi=200, bbox_inches='tight')
    plt.show()

    # Plot absolute error vs N (log-log) with N^{-1/2} reference
    plt.figure(figsize=(8, 5))
    plt.loglog(Ns, abs_errors, 'o', label=r'|I_N - I_exact|')

    # Reference ~ C / sqrt(N)
    C = abs_errors[-1] * np.sqrt(Ns[-1])
    ref = C / np.sqrt(Ns)
    plt.loglog(Ns, ref, '--', label=r'Reference $\propto N^{-1/2}$')

    plt.xlabel('Number of samples N (log scale)')
    plt.ylabel('Absolute error (log scale)')
    plt.title('MC error scaling ~ N^{-1/2} (Group A)')
    plt.grid(True, which='both', linestyle=':')
    plt.legend()
    plt.tight_layout()
    plt.savefig('GroupA_MC_convergence_error.png', dpi=200, bbox_inches='tight')
    plt.show()
"""