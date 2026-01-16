import numpy as np
import math
import matplotlib.pyplot as plt

# ---------------------------
# Data from Table I (even-even)
# (parent, Q_alpha in MeV, log10(T1/2)_exp in s)
# ---------------------------
raw_data = [
    ("146Sm", 2.53, 15.33),
    ("150Gd", 2.81, 13.75),
    ("150Dy", 4.35,  3.07),
    ("154Dy", 2.95, 13.98),
    ("154Er", 4.28,  4.68),
    ("154Yb", 5.47, -0.35),
    ("158Yb", 4.17,  6.63),
    ("158Hf", 5.41,  0.35),
    ("162Hf", 4.42,  5.69),
    ("158W",  6.62, -2.90),
    ("162W",  5.68,  0.42),
    ("166W",  4.86,  4.74),
    ("180W",  2.52, 25.75),
    ("166Os", 6.14, -0.53),
    ("170Os", 5.54,  1.89),
    ("174Os", 4.87,  5.25),
    ("166Pt", 7.29, -3.52),
    ("172Pt", 6.46, -1.00),
    ("176Pt", 5.89,  1.20),
    ("180Pt", 5.24,  4.27),
    ("184Pt", 4.60,  7.77),
    ("188Pt", 4.01, 12.53),
    ("172Hg", 7.53, -3.64),
]

# proton number for each element
Z_MAP = {
    "Sm": 62, "Gd": 64, "Dy": 66, "Er": 68, "Yb": 70,
    "Hf": 72, "W": 74,  "Os": 76, "Pt": 78, "Hg": 80,
}

def parse_parent(label):
    # split e.g. "146Sm" -> A=146 and symbol "Sm"
    i = 0
    while i < len(label) and label[i].isdigit():
        i += 1
    A = int(label[:i])
    sym = label[i:]
    Z = Z_MAP[sym]
    return A, Z, sym

def classify_case(A, Z):
    # decide even-even / evenZ-oddN / oddZ-evenN / odd-odd
    N = A - Z
    if Z % 2 == 0 and N % 2 == 0:
        return "even-even"
    elif Z % 2 == 0 and N % 2 == 1:
        return "evenZ-oddN"
    elif Z % 2 == 1 and N % 2 == 0:
        return "oddZ-evenN"
    else:
        return "odd-odd"

def royer_params(case_name):
    # (a, b, c) for Royer Eq.(2)
    if case_name == "even-even":
        return -25.31, -1.1629, 1.5864
    elif case_name == "evenZ-oddN":
        return -26.65, -1.0859, 1.5848
    elif case_name == "oddZ-evenN":
        return -25.68, -1.1423, 1.592
    else:  # odd-odd
        return -29.48, -1.113, 1.6971

def royer_logT(A, Z, Q, case_name):
    a, b, c = royer_params(case_name)
    return a + b * (A ** (1/6)) * math.sqrt(Z) + c * Z / math.sqrt(Q)

# ---------------------------
# Put data into arrays
# ---------------------------
n = len(raw_data)
parents = []
A_arr = np.zeros(n, int)
Z_arr = np.zeros(n, int)
Q_arr = np.zeros(n, float)
logT_exp = np.zeros(n, float)
cases = []

for i, (lab, Q, logT) in enumerate(raw_data):
    A, Z, sym = parse_parent(lab)
    parents.append(lab)
    A_arr[i] = A
    Z_arr[i] = Z
    Q_arr[i] = Q
    logT_exp[i] = logT
    cases.append(classify_case(A, Z))

# ---------------------------
# Geiger–Nuttall fit using experimental data:
# log10(T1/2) = a * (1/sqrt(Q)) + b
# ---------------------------
x = 1/np.sqrt(Q_arr)
a_gn, b_gn = np.polyfit(x, logT_exp, 1)

print("GN fit from experimental data:")
print(f"a = {a_gn:.4f}")
print(f"b = {b_gn:.4f}")
print()

# GN and Royer predictions
logT_gn = a_gn * x + b_gn
logT_royer = np.zeros(n)
for i in range(n):
    logT_royer[i] = royer_logT(A_arr[i], Z_arr[i], Q_arr[i], cases[i])

# ---------------------------
# Simple table
# ---------------------------
print("Parent  A   Z   Q(MeV)  logT_exp   logT_GN   logT_Royer")
for i in range(n):
    print(f"{parents[i]:>6} {A_arr[i]:3d} {Z_arr[i]:3d} "
          f"{Q_arr[i]:6.2f} {logT_exp[i]:9.2f} {logT_gn[i]:9.2f} {logT_royer[i]:11.2f}")

# ---------------------------
# Plot 1: log10(T1/2) vs Q_alpha
# ---------------------------
order = np.argsort(Q_arr)
Q_sorted = Q_arr[order]

plt.figure()
plt.scatter(Q_arr, logT_exp,    label="Exp",   marker="o")
plt.scatter(Q_arr, logT_gn,     label="GN",    marker="s")
plt.scatter(Q_arr, logT_royer,  label="Royer", marker="^")

plt.plot(Q_sorted, logT_exp[order],   "-",  label="Exp curve")
plt.plot(Q_sorted, logT_gn[order],    "--", label="GN curve")
plt.plot(Q_sorted, logT_royer[order], ":",  label="Royer curve")

plt.xlabel("Qα (MeV)")
plt.ylabel("log10(T1/2 / s)")
plt.title("log10(T1/2) vs Qα")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ---------------------------
# Plot 2: log10(T1/2) vs 1/sqrt(Q_alpha)
# with best-fit lines for Exp and Royer
# ---------------------------
plt.figure()
plt.scatter(x, logT_exp,   label="Exp",   marker="o")
plt.scatter(x, logT_gn,    label="GN",    marker="s")
plt.scatter(x, logT_royer, label="Royer", marker="^")

# experimental best-fit (same as GN fit)
x_line = np.linspace(x.min(), x.max(), 200)
y_exp_fit = a_gn * x_line + b_gn
plt.plot(x_line, y_exp_fit, "k-", label="Exp best fit")

# Royer best-fit line
a_roy, b_roy = np.polyfit(x, logT_royer, 1)
y_roy_fit = a_roy * x_line + b_roy
plt.plot(x_line, y_roy_fit, "g--", label="Royer best fit")

print()
print("Best-fit (Exp):   log10(T1/2) = {:.4f} * 1/sqrt(Q) + {:.4f}".format(a_gn, b_gn))
print("Best-fit (Royer): log10(T1/2) = {:.4f} * 1/sqrt(Q) + {:.4f}".format(a_roy, b_roy))

plt.xlabel("1/√Qα  (MeV$^{-1/2}$)")
plt.ylabel("log10(T1/2 / s)")
plt.title("log10(T1/2) vs 1/√Qα")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
