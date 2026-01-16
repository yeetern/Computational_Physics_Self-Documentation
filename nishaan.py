import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# 1. YOUR DATA
# ======================

data = [
    ["146Sm → 142Nd", 2.53, 15.33, 15.45, 146, 62],
    ["150Gd → 146Sm", 2.81, 13.75, 13.77, 150, 64],
    ["150Dy → 146Gd", 4.35, 3.07, 2.92, 150, 66],
    ["154Dy → 150Gd", 2.95, 13.98, 13.77, 154, 66],
    ["154Er → 150Dy", 4.28, 4.68, 4.48, 154, 68],
    ["154Yb → 150Er", 5.47, -0.35, -0.57, 154, 70],
    ["158Yb → 154Er", 4.17, 6.63, 6.33, 158, 70],
    ["158Hf → 154Yb", 5.41, 0.35, 0.71, 158, 72],
    ["162Hf → 158Yb", 4.42, 5.69, 5.90, 162, 72],
    ["158W → 154Hf", 6.62, -2.90, -3.13, 158, 74],
    ["162W → 158Hf", 5.68, 0.42, 0.45, 162, 74],
    ["166W → 162Hf", 4.86, 4.74, 4.41, 166, 74],
    ["180W → 176Hf", 2.52, 25.75, 25.10, 180, 74],
    ["166Os → 162W", 6.14, -0.53, -0.58, 166, 76],
    ["170Os → 166W", 5.54, 1.89, 1.95, 170, 76],
    ["174Os → 170W", 4.87, 5.25, 5.30, 174, 76],
    ["166Pt → 162Os", 7.29, -3.52, -3.71, 166, 78],
    ["172Pt → 168Os", 6.46, -1.00, -0.99, 172, 78],
    ["176Pt → 172Os", 5.89, 1.20, 1.28, 176, 78],
    ["180Pt → 176Os", 5.24, 4.27, 4.30, 180, 78],
    ["184Pt → 180Os", 4.60, 7.77, 7.88, 184, 78],
    ["188Pt → 184Os", 4.01, 12.53, 11.97, 188, 78],
    ["172Hg → 168Pt", 7.53, -3.64, -3.73, 172, 80]
]

# ======================
# 2. EXTRACT DATA FOR GEIGER-NUTTALL FITTING
# ======================

Q_vals = np.array([row[1] for row in data])
logT_exp_vals = np.array([row[2] for row in data])
A_vals = np.array([row[4] for row in data])
Z_vals = np.array([row[5] for row in data])

# Fit Geiger-Nuttall from experimental data
x_vals = 1 / np.sqrt(Q_vals)
coeff_GN = np.polyfit(x_vals, logT_exp_vals, 1)
a_GN, b_GN = coeff_GN[0], coeff_GN[1]

# ======================
# 3. DEFINE THE FORMULAS
# ======================

def geiger_nuttall(Q, a=a_GN, b=b_GN):
    """Geiger-Nuttall Law with coefficients from experimental data"""
    return a * (1/np.sqrt(Q)) + b

def royer_formula(Q, Z, A):
    """Royer formula with paper coefficients for even-even nuclei"""
    a, b, c = -25.31, -1.1629, 1.5864
    return a + b * (A**(1/6)) * np.sqrt(Z) + c * Z / np.sqrt(Q)

# ======================
# 4. CALCULATIONS
# ======================

results = []

for row in data:
    decay = row[0]
    Q = row[1]           # Qα in MeV
    logT_exp = row[2]    # Experimental logT
    logT_paper = row[3]  # Paper's calculated logT
    A = row[4]           # Mass number
    Z = row[5]           # Proton number
    
    # Calculate using Geiger-Nuttall with fitted coefficients
    logT_GN = geiger_nuttall(Q)
    
    # Calculate using Royer formula (paper coefficients)
    logT_Royer = royer_formula(Q, Z, A)
    
    # Convert to actual half-life in seconds
    T_exp = 10**logT_exp
    T_GN = 10**logT_GN
    T_Royer = 10**logT_Royer
    T_paper = 10**logT_paper
    
    results.append({
        "Decay": decay,
        "Q (MeV)": Q,
        "logT_exp": logT_exp,
        "logT_GN": logT_GN,
        "logT_Royer": logT_Royer,
        "logT_paper": logT_paper,
        "T_exp (s)": T_exp,
        "T_GN (s)": T_GN,
        "T_Royer (s)": T_Royer,
        "T_paper (s)": T_paper,
    })

df = pd.DataFrame(results)

# ======================
# 5. CREATE CLEAN TABLE (SAME FORMAT AS BEFORE)
# ======================

print("=" * 100)
print("α-DECAY HALF-LIVES CALCULATIONS")
print("=" * 100)
print("\nComparison of Experimental and Calculated Values")
print("-" * 100)

# Display table with Q-values and half-lives (SAME FORMAT AS BEFORE)
display_cols = ["Decay", "Q (MeV)", "logT_exp", "logT_GN", "logT_Royer", "logT_paper",
                "T_exp (s)", "T_GN (s)", "T_Royer (s)", "T_paper (s)"]
display_df = df[display_cols].copy()

# Format the scientific notation nicely
pd.set_option('display.float_format', lambda x: f'{x:.2e}' if abs(x) < 0.01 or abs(x) > 1000 else f'{x:.2f}')

print(display_df.to_string(index=False))

# ======================
# 6. PRINT MODEL EQUATIONS
# ======================

print("\n" + "=" * 70)
print("MODEL EQUATIONS")
print("=" * 70)
print(f"\nGeiger-Nuttall Law (fitted from experimental data):")
print(f"  log₁₀(T₁/₂) = {a_GN:.4f} × Q⁻¹/² + {b_GN:.4f}")

print(f"\nRoyer Formula (paper coefficients for even-even nuclei):")
print(f"  log₁₀(T₁/₂) = -25.31 - 1.1629 × A¹/⁶ × √Z + 1.5864 × Z/√Q")

# ======================
# 7. PLOT: Geiger-Nuttall Plot
# ======================

plt.figure(figsize=(10, 6))

# Calculate 1/sqrt(Q) for x-axis
df['1/sqrt(Q)'] = 1 / np.sqrt(df['Q (MeV)'])

# Plot experimental data
plt.scatter(df['1/sqrt(Q)'], df['logT_exp'], color='black', s=100, 
           label='Experimental', zorder=5, marker='o', edgecolors='black')

# Plot Geiger-Nuttall calculations
plt.scatter(df['1/sqrt(Q)'], df['logT_GN'], color='red', s=80, 
           label='Geiger-Nuttall', alpha=0.8, marker='^')

# Plot Royer calculations (paper coefficients)
plt.scatter(df['1/sqrt(Q)'], df['logT_Royer'], color='blue', s=80, 
           label='Royer Formula', alpha=0.8, marker='s')

# Plot Paper's calculations
plt.scatter(df['1/sqrt(Q)'], df['logT_paper'], color='green', s=80, 
           label='Paper Calculation', alpha=0.6, marker='d')

# Add labels for some key nuclei
for idx, row in df.iterrows():
    if idx % 3 == 0:  # Label every 3rd nucleus to avoid clutter
        plt.annotate(row['Decay'].split("→")[0].strip(), 
                    (row['1/sqrt(Q)'], row['logT_exp']), 
                    xytext=(5, 5), textcoords='offset points', 
                    fontsize=8, alpha=0.7)

# Add linear regression line for Geiger-Nuttall law
x_line = np.linspace(df['1/sqrt(Q)'].min(), df['1/sqrt(Q)'].max(), 100)
y_line = a_GN * x_line + b_GN
plt.plot(x_line, y_line, 'r--', alpha=0.7, linewidth=2, 
         label=f'Geiger-Nuttall: y={a_GN:.2f}x+{b_GN:.2f}')

# Add Royer trendline (paper coefficients)
# For average Z and A, show Royer's dependence on 1/√Q
avg_Z = np.mean(Z_vals)
avg_A = np.mean(A_vals)
a_R, b_R, c_R = -25.31, -1.1629, 1.5864
fixed_term_Royer = a_R + b_R * (avg_A**(1/6)) * np.sqrt(avg_Z)
slope_Royer = c_R * avg_Z
y_Royer_trend = fixed_term_Royer + slope_Royer * x_line
plt.plot(x_line, y_Royer_trend, 'b--', alpha=0.7, linewidth=2, 
         label=f'Royer: slope={slope_Royer:.1f}')

plt.xlabel('$1/\sqrt{Q_{\\alpha}}$ (MeV$^{-1/2}$)', fontsize=12)
plt.ylabel('$\log_{10}(T_{1/2})$ (s)', fontsize=12)
plt.title(f'Geiger-Nuttall Plot: $\log_{{10}}(T_{{1/2}})$ vs $1/\sqrt{{Q_{{\\alpha}}}}$\n' +
          f'Geiger-Nuttall: $\log_{{10}}T = {a_GN:.2f}Q^{{-1/2}} + {b_GN:.2f}$', fontsize=13)
plt.legend(loc='best', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ======================
# 8. SUMMARY STATISTICS
# ======================

print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

# Calculate differences
df['diff_GN'] = df['logT_GN'] - df['logT_exp']
df['diff_Royer'] = df['logT_Royer'] - df['logT_exp']
df['diff_paper'] = df['logT_paper'] - df['logT_exp']

print(f"\nAverage logT values:")
print(f"  Experimental: {df['logT_exp'].mean():.2f}")
print(f"  Geiger-Nuttall: {df['logT_GN'].mean():.2f}")
print(f"  Royer Formula: {df['logT_Royer'].mean():.2f}")
print(f"  Paper: {df['logT_paper'].mean():.2f}")

print(f"\nStandard Deviation of logT values:")
print(f"  Experimental: {df['logT_exp'].std():.2f}")
print(f"  Geiger-Nuttall: {df['logT_GN'].std():.2f}")
print(f"  Royer Formula: {df['logT_Royer'].std():.2f}")
print(f"  Paper: {df['logT_paper'].std():.2f}")

# Calculate mean absolute errors
mae_GN = np.mean(np.abs(df['diff_GN']))
mae_Royer = np.mean(np.abs(df['diff_Royer']))
mae_paper = np.mean(np.abs(df['diff_paper']))

print(f"\nMean Absolute Error (log units):")
print(f"  Geiger-Nuttall: {mae_GN:.4f}")
print(f"  Royer Formula:  {mae_Royer:.4f}")
print(f"  Paper's calc:   {mae_paper:.4f}")

# Calculate correlation with experimental values
corr_GN = np.corrcoef(df['logT_GN'], df['logT_exp'])[0,1]
corr_Royer = np.corrcoef(df['logT_Royer'], df['logT_exp'])[0,1]
corr_paper = np.corrcoef(df['logT_paper'], df['logT_exp'])[0,1]

print(f"\nCorrelation with experimental values:")
print(f"  Geiger-Nuttall: {corr_GN:.4f}")
print(f"  Royer Formula:  {corr_Royer:.4f}")
print(f"  Paper's calc:   {corr_paper:.4f}")

# Show range of Q-values
print(f"\nQ-value Range: {df['Q (MeV)'].min():.2f} to {df['Q (MeV)'].max():.2f} MeV")
print(f"Corresponding T1/2 range: {df['T_exp (s)'].min():.2e} to {df['T_exp (s)'].max():.2e} s")

# ======================
# 9. FINAL COEFFICIENT SUMMARY
# ======================

print("\n" + "=" * 70)
print("FINAL GEIGER-NUTTALL COEFFICIENTS")
print("=" * 70)
print(f"\nBased on {len(data)} experimental data points:")
print(f"  a = {a_GN:.8f}")
print(f"  b = {b_GN:.8f}")
print(f"\nUse this equation for your dataset:")
print(f"  log₁₀(T₁/₂) = {a_GN:.3f} × Q⁻¹/² + {b_GN:.3f}")