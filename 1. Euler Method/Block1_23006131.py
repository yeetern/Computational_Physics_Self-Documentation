#Assignment 1 Block 1
#Program Name: Euler Method for dy/dt = 2y(1 - y)
#Subject: SIF3012 Computational Physics
#Author: Tan Yee Tern
#Student ID: 23006131
#Email: 23006131@siswa.um.edu.my
#Date of Creation: Thursday October 30

#Description:
#This program applies Euler’s method to approximate the solution of the differential
#equation dy/dt = 2y(1 - y), where y(0) is given by the last two digits of the metric number
#divided by 100. The program uses a step size h = 0.125 to compute y(0.125) and y(0.25).
#It compares the result with the exact analytical solution of the logistic equation.

#Comment:
#Dear Dr. Juan, I plan to save my code on Github for documentation propose.
#So, the coding will include some extra function that I put # in front of the code
#such as compute the actual/exact value and the comparison.
#Please feel free to give any comment/advice for the coding.

#--------------------------------------------------------------------------------------------

#Exercise 1
import math

#user input
l2d = int(input("Enter the last 2 digits for the number: "))

def f(y):
    return 2*y*(1-y) #can sub any function for similar problem

y0 = l2d/100
print(f"The Initial Condition, y0= {y0}")

h = 0.125 #can sub with any step size

#Euler Method
y1 = y0 + h * f(y0)
y2 = y1 + h * f(y1)

#Print Result
print(f"y(0.125) = {y1:6f}")
print(f"y(0.25) = {y2:6f}")

#----------------------------------------------------------------------------
#Extra codding for compare as below
#print("\nBelow is Extra Comparison")
#Exact Solution
#def y_exact(t, y0):
    #return 1 / (1 + ((1 / y0) - 1) * math.exp(-2 * t))

#Calculate exact values for comparison
#ye1 = y_exact(0.125, y0)
#ye2 = y_exact(0.25, y0)

#print("\nExact Solution Comparison:")
#print(f"y_exact(0.125) = {ye1:.6f}")
#print(f"y_exact(0.25)  = {ye2:.6f}")

#print("\nDifferences:")
#print(f"|Error at 0.125| = {abs(y1 - ye1):.6e}")
#print(f"|Error at 0.25|  = {abs(y2 - ye2):.6e}")
#--------------------------------------------------------------------------------

print("\nProgram finished.")
#End of Program

#--------------------------------------------------------------------------------
#Exercise 2
import math

#user input
l2d = int(input("Enter the last 2 digits for the number: "))

def f(y):
    return 2*y*(1-y) #can sub any function for similar problem

y0 = l2d/100
print(f"The Initial Condition, y0= {y0}")

h = 0.125 #can sub with any step size
tf = 10 #also can ask user to input
n = int(tf / h) #number of steps/iteration

#Euler’s method loop
y = y0 #define new y to avoid confused
t = 0.0

#Extra print out table
#print("Below is the table for iteration:\n      Step        y")

for i in range(n):
    y = y + h * f(y)
    t += h
    #print(f"\n   {t}     {y}")

print(f"\nAfter {n} steps (t = {tf}):")
print(f"Euler approximation y(10) = {y:.6f}")

#--------------------------------------------------------------------------------
#Extra Comparisom
#Exact logistic solution for comparison
#def y_exact(t, y0):
    #return 1 / (1 + ((1 / y0) - 1) * math.exp(-2 * t))

#y_true = y_exact(10, y0)
#print(f"Exact solution y_exact(10) = {y_true:.6f}")
#print(f"Absolute error = {abs(y - y_true):.6e}")
#--------------------------------------------------------------------------------

print("\nProgram finished.")
#End of program

#--------------------------------------------------------------------------------
#Exercise 3
#Same as Exercise 2, just change the steps size, h
import math

#user input
l2d = int(input("Enter the last 2 digits for the number: "))

def f(y):
    return 2*y*(1-y) #can sub any function for similar problem

y0 = l2d/100
print(f"The Initial Condition, y0= {y0}")

h = 0.00125 #can sub with any step size
tf = 10 #also can ask user to input
n = int(tf / h) #number of steps/iteration

#Euler’s method loop
y = y0 #define new y to avoid confused
t = 0.0

for i in range(n):
    y = y + h * f(y)
    t += h

print(f"\nAfter {n} steps (t = {tf}):")
print(f"Euler approximation y(10) = {y:.6f}")

#--------------------------------------------------------------------------------
#Extra Comparisom
#Exact logistic solution for comparison
#def y_exact(t, y0):
    #return 1 / (1 + ((1 / y0) - 1) * math.exp(-2 * t))

#y_true = y_exact(10, y0)
#print(f"Exact solution y_exact(10) = {y_true:.6f}")
#print(f"Absolute error = {abs(y - y_true):.6e}")
#--------------------------------------------------------------------------------

print("\nProgram finished.")
#End of program
#--------------------------------------------------------------------------------
# Exercise 4
import argparse, math, os, sys
import numpy as np
import matplotlib.pyplot as plt

# Define function
def f(y: float) -> float:
    return 2.0 * y * (1.0 - y)

def euler(y0: float, h: float, tf: float):
    n = int(round(tf / h))
    y = y0
    t = 0.0
    ts = [t]
    ys = [y]
    for _ in range(n):
        y = y + h * f(y)
        t += h
        ts.append(t)
        ys.append(y)
    return np.array(ts), np.array(ys)

def y_exact(t, y0: float):
    t = np.asarray(t, dtype=float)
    return 1.0 / (1.0 + ((1.0 / y0) - 1.0) * np.exp(-2.0 * t))

# Command-Line Interface (CLI)
def parse_args():
    p = argparse.ArgumentParser(description="Exercise 4: Euler vs exact for dy/dt = 2y(1-y)")
    p.add_argument("--l2d", type=int, help="Last two digits of metric no. (e.g., 50 => y0=0.50)")
    p.add_argument("--no-show", action="store_true", help="Do not pop interactive windows")
    return p.parse_args()

# Define plot style
def set_pub_style():
    plt.rcParams.update({
        "figure.figsize": (8, 5),
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.alpha": 0.4,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 10,
        "lines.linewidth": 2.5,
        "savefig.dpi": 300,
    })

# Main
def main():
    args = parse_args() #Retrieve CLI
    if args.l2d is None:
        try:
            args.l2d = int(input("Enter the last 2 digits for the number: ")) #user input
        except Exception:
            print("Invalid input; defaulting to 50.") #If user input alphabet, will default y0 = 0.50
            args.l2d = 50

    set_pub_style()

    # Problem setup
    y0 = args.l2d / 100.0
    tf = 10.0
    h_coarse = 0.125
    h_fine   = 0.00125

    # Compute Euler trajectories
    t_coarse, y_coarse = euler(y0, h_coarse, tf)
    t_fine,   y_fine   = euler(y0, h_fine,   tf)

    # Exact trajectories on dense and Euler grids
    t_dense = np.linspace(0.0, tf, 2001)
    y_dense = y_exact(t_dense, y0)
    y_exact_coarse = y_exact(t_coarse, y0)
    y_exact_fine   = y_exact(t_fine,   y0)

    # Summary at t = 10
    y10_true   = float(y_exact(tf, y0))
    y10_coarse = float(y_coarse[-1])
    y10_fine   = float(y_fine[-1])
    err_coarse = abs(y10_coarse - y10_true)
    err_fine   = abs(y10_fine   - y10_true)

    print("\nExercise 4 — y(10) comparison (y0 = {:.2f})".format(y0))
    print("{:<20} {:>14} {:>20}".format("Method", "y(10)", "Abs. Error vs Exact"))
    row = "{:<20} {:>14.8f} {:>20.3e}"
    print(row.format("Euler (h = 0.125)",  y10_coarse, err_coarse))
    print(row.format("Euler (h = 0.00125)",y10_fine,   err_fine))
    print(row.format("Exact",              y10_true,   0.0))

    # ---------------- Plot 1: solution curves ----------------
    plt.figure()
    # exact (black), h=0.125 (blue line), h=0.00125 (orange line)
    plt.plot(t_dense,  y_dense,  label="Exact solution", color="black", linewidth=3)
    plt.plot(t_coarse, y_coarse, label="Euler h = 0.125", color="tab:blue")
    plt.plot(t_fine,   y_fine,   label="Euler h = 0.00125", color="tab:orange")

    plt.xlabel("Time, $t$ (seconds)")
    plt.ylabel("Solution, $y(t)$")
    plt.title(r"Solution of $\frac{dy}{dt}=2y(1-y)$ Using Euler Method")
    # Put legend outside (right)
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0.0)
    plt.xlim(0, tf)
    plt.ylim(0, 1.02)
    plt.tight_layout()
    # Save Png
    #sol_png = "solution_curves_publication.png"
    #plt.savefig(sol_png, bbox_inches="tight")
    #print(f"Saved plot: {os.path.abspath(sol_png)}")
    if not args.no_show:
        plt.show()

    # ---------------- Plot 2: absolute error vs time ----------------
    err_curve_coarse = np.abs(y_coarse - y_exact_coarse)
    err_curve_fine   = np.abs(y_fine   - y_exact_fine)

    plt.figure()
    plt.plot(t_coarse, err_curve_coarse, label="|error|, h = 0.125", color="tab:blue")
    plt.plot(t_fine,   err_curve_fine,   label="|error|, h = 0.00125", color="tab:orange")
    plt.yscale("log")
    plt.xlabel("Time, $t$ (seconds)")
    plt.ylabel(r"Absolute Error, $|\,y(t)-y_{\mathrm{exact}}(t)\,|$")
    plt.title("Euler Method Global Error vs Time")
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0.0)
    plt.xlim(0, tf)
    # avoid zero on log-axis
    ymin = min(err_curve_coarse.min(), err_curve_fine.min())
    plt.ylim(max(ymin*0.5, 1e-16), 1e-1)
    plt.tight_layout()
    # Save Png
    #err_png = "error_plot_publication.png"
    #plt.savefig(err_png, bbox_inches="tight")
    #print(f"Saved plot: {os.path.abspath(err_png)}")
    if not args.no_show:
        plt.show()

if __name__ == "__main__":
    sys.exit(main())

#Yes,  there are any significant differences. The y0 I using are 0.01 and 0.50.
#The Euler solutions for step sizes h=0.125 and h=0.00125 were compared against 
#the exact solution for two initial values, y0=0.01 and y0=0.50. In both cases, 
#the fine-step solution closely matches the analytical trajectory while the coarse-step
#solution exhibits a noticeable lag during the rapid growth phase, confirming the
#expected first-order accuracy of the Euler method. The difference is far more pronounced
#for y0=0.01, because the system begins near zero and undergoes a steeper transient,
#making numerical errors visibly larger before saturation at y=1. In contrast, for 
#y0=0.50 the solution quickly approaches equilibrium, so the curves nearly overlap
#and error remains visually subtle. Therefore, using y0=0.01 provides a clearer
#demonstration of numerical convergence behavior, whereas y0=0.50 produces 
#less distinguishable curves due to rapid stabilization.

#PS: There's still has some bug for my code such as
#When user input more than 2 integer, like 1234,
#y0 will become 12.34 which is not only 2 integer.
#Also I default y0=0.50 if input are not integer. (i.e abcd, 1.234)
#As a physicist, do we really need to consider this?
#Thank you Dr. Juan for taking the time to review and assess this work.
#Constructive comments or suggestions to improve coding style
#and numerical practice are sincerely appreciated.
