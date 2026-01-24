import numpy as np
import matplotlib.pyplot as plt

ME_C2_KEV = 511.0  # electron rest energy in keV


def mu_photo(E_keV, mu_photo_ref, E_ref_keV, power=3.0):
    """Simple model: photoelectric μ roughly decreases steeply with energy."""
    E = max(E_keV, 1e-6)
    return mu_photo_ref * (E / E_ref_keV) ** (-power)


def mu_compton(E_keV, mu_compton_ref):
    """Simple model: Compton μ is weakly energy dependent -> constant baseline."""
    _ = E_keV
    return mu_compton_ref


def klein_nishina_pdf_cos_theta(cos_theta, E_keV):
    """
    Klein–Nishina differential cross-section (shape only) as a function of cosθ.

    Using:
      k = E / (m_e c^2)
      E'/E = 1 / (1 + k(1 - cosθ)) = r
      dσ/dΩ ∝ r^2 (r + 1/r - sin^2θ)
    """
    k = E_keV / ME_C2_KEV
    r = 1.0 / (1.0 + k * (1.0 - cos_theta))
    sin2 = 1.0 - cos_theta**2
    val = (r**2) * (r + 1.0 / r - sin2)
    return max(val, 0.0)


def sample_cos_theta_kn(E_keV, rng, n_try_max=10_000):
    """
    Rejection sampling for cosθ in [-1, 1] using a safe envelope.

    For the acceptance test we need a bound on pdf.
    A simple bound is to scan a small grid once per call and use its max.
    That's not fastest but is stable and clear for a student project.
    """
    # Estimate max on a coarse grid
    grid = np.linspace(-1.0, 1.0, 200)
    pdf_vals = np.array([klein_nishina_pdf_cos_theta(c, E_keV) for c in grid])
    pdf_max = pdf_vals.max()
    if pdf_max <= 0:
        return 1.0  # fallback: forward

    for _ in range(n_try_max):
        c = rng.uniform(-1.0, 1.0)
        y = rng.uniform(0.0, pdf_max)
        if y <= klein_nishina_pdf_cos_theta(c, E_keV):
            return c

    # If rejection sampling fails (rare), fall back to forward scatter
    return 1.0


def compton_scattered_energy(E_keV, cos_theta):
    """Compton formula: E' = E / (1 + (E/mc^2)(1 - cosθ))."""
    k = E_keV / ME_C2_KEV
    return E_keV / (1.0 + k * (1.0 - cos_theta))

# Monte Carlo simulation
def simulate_photons(
    N=1000,
    E0_keV=662.0,
    thickness_cm=5.0,
    dx_cm=0.01,
    mu_photo_ref=0.40,     # 1/cm at E_ref (rough placeholder)
    mu_compton_ref=0.10,   # 1/cm (rough placeholder)
    E_ref_keV=662.0,
    photo_power=3.0,
    energy_loss=True,
    seed=42
):
    """
    Returns:
      thickness_grid (cm),
      I_over_I0 (array),
      absorbed_depths (array of absorption depths in cm),
      transmitted_mask (bool array of length N),
      mu_ref_total (float) reference μ at E0 used for theory HVL
    """

    rng = np.random.default_rng(seed)

    # Store absorption depth; if transmitted, set to np.inf (survived whole slab)
    absorb_depth = np.full(N, np.inf, dtype=float)

    steps = int(np.ceil(thickness_cm / dx_cm))
    thickness_grid = np.linspace(0.0, thickness_cm, steps + 1)

    # Reference μ at E0 (for theory HVL comparison)
    mu_ref_total = mu_photo(E0_keV, mu_photo_ref, E_ref_keV, photo_power) + mu_compton(E0_keV, mu_compton_ref)

    for n in range(N):
        x = 0.0
        E = E0_keV
        alive = True

        for _ in range(steps):
            if not alive:
                break

            # Current macroscopic coefficients
            mu_p = mu_photo(E, mu_photo_ref, E_ref_keV, photo_power)
            mu_c = mu_compton(E, mu_compton_ref)
            mu_t = mu_p + mu_c

            # Probability at least one interaction in dx (Poisson)
            p_int = 1.0 - np.exp(-mu_t * dx_cm)

            r = rng.random()
            if r < p_int:
                # An interaction occurs, choose type by relative rates
                if rng.random() < (mu_p / mu_t):
                    # Photoelectric absorption (photon dies here)
                    alive = False
                    absorb_depth[n] = x  # absorbed at current depth
                else:
                    # Compton scatter: update energy if enabled
                    if energy_loss:
                        cos_th = sample_cos_theta_kn(E, rng)
                        E = compton_scattered_energy(E, cos_th)
                        # Optional: if energy becomes too low, absorption dominates anyway
                        E = max(E, 1e-3)
                    # In 1D model, photon continues forward after scattering
                    x += dx_cm
            else:
                # No interaction
                x += dx_cm

            if x >= thickness_cm - 1e-12:
                break

        # If alive until exiting the slab, absorb_depth remains np.inf

    # Intensity at thickness x is count of photons with absorb_depth > x
    I = np.array([(absorb_depth > x).sum() for x in thickness_grid], dtype=float)
    I_over_I0 = I / I[0]

    transmitted_mask = np.isinf(absorb_depth)
    absorbed_depths = absorb_depth[~transmitted_mask]

    return thickness_grid, I_over_I0, absorbed_depths, transmitted_mask, mu_ref_total


def find_hvl(thickness_grid, I_over_I0):
    """Linear interpolation for HVL where I/I0 = 0.5."""
    target = 0.5
    y = I_over_I0
    x = thickness_grid

    if y.min() > target:
        return np.nan  # not enough thickness to reach half

    # Find first index where y <= target
    idx = np.where(y <= target)[0]
    if len(idx) == 0:
        return np.nan
    i = idx[0]
    if i == 0:
        return x[0]

    # Interpolate between i-1 and i
    x0, y0 = x[i - 1], y[i - 1]
    x1, y1 = x[i], y[i]
    if abs(y1 - y0) < 1e-12:
        return x1
    return x0 + (target - y0) * (x1 - x0) / (y1 - y0)

# Main (user I/O + plots)
def main():
    print("\n=== Virtual Lead Wall (Monte Carlo Light) ===\n")

    # Basic user inputs
    try:
        N = int(input("Number of photons N (e.g., 1000): ").strip() or "1000")
        E0 = float(input("Initial gamma energy E0 in keV (e.g., 662 for Cs-137): ").strip() or "662")
        thickness = float(input("Shield thickness in cm (e.g., 5): ").strip() or "5")
        dx = float(input("Step size dx in cm (e.g., 0.01): ").strip() or "0.01")

        print("\nSet reference attenuation coefficients at E0 (units: 1/cm).")
        mu_p_ref = float(input("mu_photo_ref at E0 (e.g., 0.40): ").strip() or "0.40")
        mu_c_ref = float(input("mu_compton_ref at E0 (e.g., 0.10): ").strip() or "0.10")

        power = float(input("Photoelectric energy power (mu_photo ~ E^{-p}), p (e.g., 3): ").strip() or "3")
    except ValueError:
        print("Invalid input. Using defaults.")
        N, E0, thickness, dx = 1000, 662.0, 5.0, 0.01
        mu_p_ref, mu_c_ref, power = 0.40, 0.10, 3.0

    # Run 2 scenarios:
    # 1) Energy loss ON (physically meaningful)
    # 2) Energy loss OFF (deliberately wrong baseline)
    x1, I1, abs_depths1, tx_mask1, mu_ref_total = simulate_photons(
        N=N, E0_keV=E0, thickness_cm=thickness, dx_cm=dx,
        mu_photo_ref=mu_p_ref, mu_compton_ref=mu_c_ref,
        E_ref_keV=E0, photo_power=power,
        energy_loss=True, seed=42
    )

    x2, I2, abs_depths2, tx_mask2, _ = simulate_photons(
        N=N, E0_keV=E0, thickness_cm=thickness, dx_cm=dx,
        mu_photo_ref=mu_p_ref, mu_compton_ref=mu_c_ref,
        E_ref_keV=E0, photo_power=power,
        energy_loss=False, seed=42
    )

    # HVL
    hvl_mc_on = find_hvl(x1, I1)
    hvl_mc_off = find_hvl(x2, I2)
    hvl_theory = (np.log(2.0) / mu_ref_total) if mu_ref_total > 0 else np.nan

    # Print summary
    print("\n=== Results ===")
    print(f"Reference mu_total at E0: {mu_ref_total:.4f} 1/cm")
    print(f"Theory HVL (ln2/mu_ref_total): {hvl_theory:.4f} cm")
    print(f"MC HVL (energy loss ON):        {hvl_mc_on:.4f} cm")
    print(f"MC HVL (energy loss OFF):       {hvl_mc_off:.4f} cm")
    print(f"Transmitted fraction (ON):      {tx_mask1.mean():.4f}")
    print(f"Transmitted fraction (OFF):     {tx_mask2.mean():.4f}")

    # Plots
    # Plot 1: I/I0 vs thickness
    plt.figure()
    plt.plot(x1, I1, label="Monte Carlo (Compton energy loss ON)")
    plt.plot(x2, I2, label="Monte Carlo (energy loss OFF)")
    plt.axhline(0.5, linestyle="--", label="Half intensity (0.5)")
    if np.isfinite(hvl_theory):
        plt.axvline(hvl_theory, linestyle="--", label="Theory HVL")
    if np.isfinite(hvl_mc_on):
        plt.axvline(hvl_mc_on, linestyle="--", label="MC HVL (ON)")
    plt.xlabel("Thickness x (cm)")
    plt.ylabel("I(x) / I0")
    plt.title("Gamma Attenuation: Intensity vs Thickness")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('intensity_vs_thickness.png')


    # Plot 2: semi-log to check approximate exponential
    plt.figure()
    # Avoid log(0)
    eps = 1e-6
    plt.semilogy(x1, np.clip(I1, eps, None), label="MC (energy loss ON)")
    plt.semilogy(x2, np.clip(I2, eps, None), label="MC (energy loss OFF)")
    plt.xlabel("Thickness x (cm)")
    plt.ylabel("log-scale: I(x) / I0")
    plt.title("Semi-log plot (exponential trend check)")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.savefig('semi-log.png')

    # Plot 3: histogram of absorption depths (energy loss ON)
    plt.figure()
    if len(abs_depths1) > 0:
        plt.hist(abs_depths1, bins=30)
    plt.xlabel("Absorption depth (cm)")
    plt.ylabel("Counts")
    plt.title("Histogram: Photon Absorption Depths (energy loss ON)")
    plt.grid(True, alpha=0.3)

    plt.savefig('radiation_histograms.png')

    plt.show()


if __name__ == "__main__":
    main()
