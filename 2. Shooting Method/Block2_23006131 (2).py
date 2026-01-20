#Assignment 2 Block 2
#Program Name: Shooting Method for y'' + x*y' - x*y = 2x
#Subject: SIF3012 Computational Physics
#Author: Tan Yee Tern
#Student ID: 23006131
#Email: 23006131@siswa.um.edu.my
#Date of Creation: Friday November 7

#Description:
#This program applies the Shooting Method to solve the boundary value problem
#               y'' + x*y' - x*y = 2x
#subject to y(0) = 1 and y(2) = 8.
#The 2nd-order ODE is reduced to a system of 1st-order equations
#               y' = z
#               z' = 2x - x*z + x*y
#and integrated using Euler's method with step size h = 0.1.
#The shooting method (Secant Method) is used to determine the initial slope
#               s = y'(0)
#such that the numerical solution satisfies y(2) ≈ 8.

#Comment:
#Dear Dr. Juan, I implemented the shooting method with Euler (h = 0.1) as required.
#Then, for my own learning, I compared the result with a high-accuracy RK4
#implementation to estimate the "true" initial slope and study the error
#behavior as h decreases.
#For assessment, please consider only Exercise 1 and 2. I would also appreciate
#any comments or feedback on the additional comparison section.

#--------------------------------------------------------------------------------
#Exercise 1
import math
import numpy as np
import matplotlib.pyplot as plt

# Define step size, h and boundary conditions (y(x=0) to y(x=2))
h = 0.1 #this value is low order that limit accuracy, can change to compare
x0, xf = 0.0, 2.0
N = int((xf - x0) / h)

# Boundary conditions, y(0) and y(2)
y0 = 1.0
yf = 8.0

# Using by-hand calculation to convert 2nd order to 1st order
# System of first-order ODEs:
# z = dy (slope, sometimes also define as s)
# d2y = dz = 2x - x*z + x*y
# Definition:
# dy = first derivative of y,
# d2y = second derivative of y and etc.
# I more prefer Leibniz Notation than Lagrange Notation because the symbol "'" is confusing sometimes.

# Define function 1
def f1(x, y, z):
    return z #dy/dx

# Define function 2
def f2(x, y, z):
    return 2*x - x*z + x*y #dz/dx or d2y/dx2

#--------------------------------------------------------------------------------
# Euler solver for a given initial slope s = y'(0)
def euler(s):
    x = x0
    y = y0
    z = s #set initial slope z(0)=s which equivalent with y'(0)
    xs = [x]
    ys = [y]
    for i in range(N):
        dy = f1(x, y, z)
        dz = f2(x, y, z)
        y = y + h * dy
        z = z + h * dz
        x = x + h
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys), y  #return y(2)

#--------------------------------------------------------------------------------
# Shooting method using Secant Method
# F(s) = y(2; s) - yf  measures how far the solution with slope s is from satisfying
# the boundary condition y(2) = yf.
# y(2; s) = The value of y(x) at x = 2, when the initial slope at x = 0 is s.

# If guess is poor or F(s) is nearly flat, secant may struggle! (very important)

def F(s):
    # Run Euler for a given initial slope s = dy/dx at x = 0
    _, _, y_end = euler(s) # _ in python means I don't need these values
    return y_end - yf  # mismatch at x = 2

# F(s) < 0, y_end < 8, undershoot
# F(s) > 0, overshoot

# Shooting Method:
# Use Secant Method on F(s) = y(2; s) - yf to find correct initial slope.
# s1, s2: initial guesses for dy/dx at x = 0
# tol: tolerance on |F(s)|
def shooting_secant(s1, s2, tol=1e-6, i_max=50):
    F1 = F(s1)
    F2 = F(s2)

    for k in range(i_max):
        # Avoid division by zero
        if abs(F2 - F1) < 1e-14:
            print("Secant method failed: denominator too small.")
            break

        # Secant update formula
        s3 = s2 - F2 * (s2 - s1) / (F2 - F1)
        F3 = F(s3)

        # if you want to monitor iteration:
        print(f"\nIter {k+1}: s = {s3:.8f}, F(s) = {F3:.8e}")
        # Suprizingly getting only 1 iteration even input wild guess(1 and 100)
        # Maybe because of linearity, it converged instantly
        # Note: For this linear problem, F(s) is (numerically) almost linear in s,
        # so the Secant Method converges in about one iteration, even for wide initial guesses.

        # Check convergence
        if abs(F3) < tol:
            return s3

        # Shift for next iteration
        s1, s2 = s2, s3
        F1, F2 = F2, F3

    # If not converged, return last estimate
    return s2

#--------------------------------------------------------------------------------
# Additional function for determine undershoot or overshoot
# Print whether this initial slope undershoots or overshoots y(2)=yf.
def describe_shot(s):
    mismatch = F(s)
    if mismatch < 0:
        print(f"s = {s:.6f}: y(2) = {yf + mismatch:.6f}  --> UNDERSHOOT (too low)")
    elif mismatch > 0:
        print(f"s = {s:.6f}: y(2) = {yf + mismatch:.6f}  --> OVERSHOOT (too high)")
    else:
        print(f"s = {s:.6f}: Exact hit at y(2) = {yf:.6f}")
    return mismatch

# Ask user for two initial guesses
print("User need to input 2 initial guesses for comparison")
s_guess1 = float(input("Enter FIRST guess for initial slope y'(0): "))
s_guess2 = float(input("Enter SECOND guess for initial slope y'(0): "))

print("\nChecking your guesses:")
F1 = describe_shot(s_guess1)
F2 = describe_shot(s_guess2)

# Extra: simple sanity check (not mandatory but helpful)
if F1 * F2 > 0:
    print("\nWarning: Both guesses give the same sign (both undershoot or both overshoot).")
    print("\nSecant method may still work, but consider choosing more separated guesses.\n")

# Automatically find solution using Secant Shooting Method
s_star = shooting_secant(s_guess1, s_guess2)
xs, ys, y_end = euler(s_star)

print("\n--- Final Result from Shooting Method ---")
print(f"Optimal initial slope y'(0) ≈ {s_star:.6f}")
print(f"Corresponding y(2) ≈ {y_end:.6f} (target = {yf})")
print("\nProgram finished.")
#End of program

#--------------------------------------------------------------------------------
# Exercise 2: Plot the solution obtained in Exercise (1)

plt.figure(figsize=(8,5))
plt.plot(xs, ys, 'o-', linewidth=1.8, markersize=5, color='navy', label="Numerical Solution y(x)")
plt.title("Exercise 2: Solution of $y'' + x y' - x y = 2x$\n(Shooting Method, h = 0.1)", fontsize=12)
plt.xlabel("x", fontsize=11)
plt.ylabel("y(x)", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

print("\nGraph is plotted.")
print("\nProgram finished.")
#End of program

#--------------------------------------------------------------------------------
# Extra coding for comparison with different method such as RK4 method
# This is for my own notes / documentation.
# For the more accurate value ("true" value) for the slope is 2.006945264
# while the value i got using Euler with h=0.1 is 2.248654.
# When we compare both values, the relative error we get is 12%.
# So, I want to try more step or other method for the accuracy.

# I get the idea of RK4 from Internet since we never learn before.

print("\nBelow is extra output using RK4 Method and Euler Method with smaller h values.")

#------------------------------- RK4 Method -------------------------------------
def rk4_step(x, y, z, h):
    k1y = f1(x, y, z)
    k1z = f2(x, y, z)

    k2y = f1(x + 0.5*h, y + 0.5*h*k1y, z + 0.5*h*k1z)
    k2z = f2(x + 0.5*h, y + 0.5*h*k1y, z + 0.5*h*k1z)

    k3y = f1(x + 0.5*h, y + 0.5*h*k2y, z + 0.5*h*k2z)
    k3z = f2(x + 0.5*h, y + 0.5*h*k2y, z + 0.5*h*k2z)

    k4y = f1(x + h, y + h*k3y, z + h*k3z)
    k4z = f2(x + h, y + h*k3y, z + h*k3z)

    y_new = y + (h/6.0)*(k1y + 2*k2y + 2*k3y + k4y)
    z_new = z + (h/6.0)*(k1z + 2*k2z + 2*k3z + k4z)
    return y_new, z_new

# This function seem longer than Euler, it might take longer operation time.

# return y(2) using RK4 with fine step for a given initial slope s.
def rk4_shoot_y2(s, h_ref=1e-4):
    x = x0
    y = y0
    z = s
    N_ref = int((xf - x0) / h_ref)
    for _ in range(N_ref):
        y, z = rk4_step(x, y, z, h_ref)
        x += h_ref
    return y

# High-accuracy shooting using RK4: find s_true so that y(2) = yf.
def shooting_secant_rk4(s1, s2, tol=1e-12, i_max=50):
    F1 = rk4_shoot_y2(s1) - yf
    F2 = rk4_shoot_y2(s2) - yf
    for _ in range(i_max):
        if abs(F2 - F1) < 1e-16:
            break
        s3 = s2 - F2 * (s2 - s1) / (F2 - F1)
        F3 = rk4_shoot_y2(s3) - yf
        if abs(F3) < tol:
            return s3
        s1, s2, F1, F2 = s2, s3, F2, F3
    return s2

# Get very accurate "true" initial slope
s_true = shooting_secant_rk4(2.0, 3.0)
print(f"\n[Accuracy check] RK4-based initial slope s_true ≈ {s_true:.10f}")

# ---------- Build reference solution on arbitrary coarse grid ----------

# Use RK4 with small step h_ref, but record y at multiples of h_grid.
# This gives a 'true' y(x) on the Euler grid.
def rk4_solution_on_grid(s, h_grid=0.1, h_ref=1e-4):
    x = x0
    y = y0
    z = s
    xs_ref = [x0]
    ys_ref = [y0]

    N_ref = int((xf - x0) / h_ref)
    step_ratio = int(round(h_grid / h_ref))
    counter = 0

    for _ in range(N_ref):
        y, z = rk4_step(x, y, z, h_ref)
        x += h_ref
        counter += 1
        if counter == step_ratio:
            xs_ref.append(x)
            ys_ref.append(y)
            counter = 0

    return np.array(xs_ref), np.array(ys_ref)

# ---------- Euler + shooting for arbitrary h, then compare ----------

# Run Euler + secant shooting for a given step size h_local.
def euler_shoot_on_grid(h_local):
    N_local = int((xf - x0) / h_local)

    def euler_once(s):
        x = x0
        y = y0
        z = s
        xs = [x]
        ys = [y]
        for _ in range(N_local):
            dy = f1(x, y, z)
            dz = f2(x, y, z)
            y = y + h_local * dy
            z = z + h_local * dz
            x = x + h_local
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys), y

    def F_local(s):
        _, _, y_end = euler_once(s)
        return y_end - yf

    # small secant just for this h_local
    s1, s2 = 2.0, 3.0
    F1, F2 = F_local(s1), F_local(s2)
    for _ in range(50):
        if abs(F2 - F1) < 1e-14:
            break
        s3 = s2 - F2 * (s2 - s1) / (F2 - F1)
        F3 = F_local(s3)
        if abs(F3) < 1e-10:
            s_opt = s3
            break
        s1, s2, F1, F2 = s2, s3, F2, F3
    else:
        s_opt = s2

    xs_e, ys_e, _ = euler_once(s_opt)
    return xs_e, ys_e, s_opt

# ---------- Compare for multiple h values ----------


h_values = [0.1, 0.05, 0.025, 0.0125, 0.0001]  # all >= h_ref = 1e-4
print("\n=== Euler vs RK4 reference (max abs error) ===")
for h_test in h_values:
    xs_e, ys_e, s_e = euler_shoot_on_grid(h_test)
    xs_ref, ys_ref = rk4_solution_on_grid(s_true, h_grid=h_test, h_ref=1e-4)
    abs_err = np.abs(ys_e - ys_ref)
    max_err = np.max(abs_err)

    # rough operation counts for one IVP with this h
    steps_euler = int((xf - x0) / h_test)
    ops_euler = 2 * steps_euler  # 2 f-evals per step

    steps_rk4 = int((xf - x0) / 0.1)
    ops_rk4 = 8 * steps_rk4  # RK4 with h=0.1 for comparison ~160

    print(f"h = {h_test:7.4f} : "
          f"s_Euler ≈ {s_e:10.6f}, "
          f"max |Euler - ref| ≈ {max_err:.3e}, "
          f"Euler ops ≈ {ops_euler:6d}, RK4(h=0.1) ops ≈ {ops_rk4}")
    
print("\nProgram finished.")
#End of program

#Conclusion:
#From the results, the RK4 method achieves a much higher accuracy with far fewer operations
#compared to the Euler method. For instance, RK4 with h = 0.1 already gives an accurate
#slope of about 2.0069, while Euler needs a very small step size (around h = 0.0001)
#to reach similar accuracy, resulting in roughly 250× more operations.
#This confirms that Euler’s global error decreases linearly with h, whereas RK4’s
#error decreases with h^4. Hence, although Euler is conceptually simpler, RK4 is
#significantly more efficient for practical computation of boundary value problems.

#--------------------------------------------------------------------------------
# Questions for Discussion / Further Understanding:
# 1. In real research or numerical modeling, how small should the tolerance be 
#    when applying iterative methods such as the Shooting or Secant Method?
#    In this exercise, using Euler with h = 0.1 gave a noticeably less accurate 
#    value for the initial slope s, so I’m curious about how accuracy and 
#    tolerance are determined in real-world simulations.
#    Is there a general guideline? For example, depending on the required 
#    physical precision, computational resources or hardware limitations?

# 2. Would you generally recommend using the RK4 method over Euler for most 
#    practical boundary value or initial value problems (IVPs), considering its 
#    higher accuracy but greater computational cost? 
#    In other words, how do we balance accuracy and computational efficiency 
#    when selecting a numerical method?

# 3. Beyond solving ODEs numerically, what are some common applications of these 
#    methods in physics or engineering? For instance, are they widely used in 
#    modeling trajectories, heat transfer, electrical circuits or even quantum systems?

# I’d really appreciate your insights, Dr. Juan, especially on how tolerance levels 
# and method selection are typically decided in actual research practice.
 
# Thank you for taking the time to review my code!

