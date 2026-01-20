#Assignment 3 Block 3
#Program Name: Finite Difference Method for y'' + x*y' - x*y = 2x
#Subject: SIF3012 Computational Physics
#Author: Tan Yee Tern
#Student ID: 23006131
#Email: 23006131@siswa.um.edu.my
#Date of Creation: Friday November 14

#Description:
#This program applies the Finite Difference Method to solve the boundary value problem
#               y'' + x*y' - x*y = 2x
#subject to y(0) = 1 and y(2) = 8.
#The numerical solution is computed using: h = 0.50 (Exercise 1) h = 0.01 (Exercise 2)
#For Exercise 1, the code constructs and displays the finite-difference matrix A
#and the right-hand side vector b representing the linear system A*y = b.
#For Exercise 2, only the numerical solution is shown (matrix omitted due to size).
#In Exercise 3, both solutions (h = 0.50 and h = 0.01) are plotted together for
#visual comparison of accuracy and discretization effects.
#Additional Feature:
#This program optionally compares three finite-difference: Forward, Backward and
#Central differences to illustrate how discretization choices affect the accuracy
#and stability of the numerical solution.

#--------------------------------------------------------------------------------
#Exercise 1

import numpy as np

# Define step size, h and boundary conditions
h   = 0.5
x0, xN = 0.0, 2.0
y0, yN = 1.0, 8.0

# Grid: x = [0.0, 0.5, 1.0, 1.5, 2.0]
x = np.arange(x0, xN + h/2, h)  # +h/2 as safe margin for stop point
N = len(x) - 1                  # last node index (here N=4)
m = N - 1                       # number of interior unknowns
# where m will be the size of matrix


# Define functions
#--------------------------- Forward Difference ---------------------------------
def forward(x, h, y0, yN):
    # create zero matrix as usual (3x3 in this case)
    A = np.zeros((m, m))
    b = np.zeros(m)

    for i in range(0, m):
        # y'  = (y_(i+1)-y_i)/h (forward)
        # y'' = (y_(i+2)-2y_(i+1)+y_i)/h**2

        xi = x[i]
        c_i   = 1/h**2 - xi/h - xi      # coeff for y_i
        c_ip1 = -2/h**2 + xi/h          # coeff for y_(i+1)
        c_ip2 = 1/h**2                  # coeff for y_(i+2)
        rhs   = 2*xi                    # right hand side
        # Simplify the equation to c_i*y_i + c_ip1*y_(i+1) + c_ip2*y_(i+2) = rhs

        # y_i
        j = i
        if 1 <= j <= N-1:               # test y_j is unknown or boundary
            A[i, j-1] += c_i            # j-1=0 represents column 0 for matrix A
        else:                           # boundary (here i=0=j, y_j=y_0)
            b[i] -= c_i * y0
            #since boundary is known, we change the equation from
            #c_i*y_0 + (unknown terms) = 2*x_i
            #to
            #(unknown terms) = 2*x_i - c_i*y_0  by moving to RHS

        # y_(i+1)
        j = i + 1
        if 1 <= j <= N-1:
            A[i, j-1] += c_ip1
        else:
            b[i] -= c_ip1 * yN

        # y_(i+2)
        j = i + 2
        if 1 <= j <= N-1:
            A[i, j-1] += c_ip2
        else:
            b[i] -= c_ip2 * yN

        #for all j part can be simplified into a simple function for high order matrix

        b[i] += rhs   #just now only minus those terms, original term (2*x_i) not added yet

    return A, b


#--------------------------- Central Difference ---------------------------------
#same logic as previous
def central(x, h, y0, yN):
    A = np.zeros((m, m))
    b = np.zeros(m)

    for i in range(0, m):
        # y'  = (y_(i+1) - y_(i-1)) / (2*h) (central)
        # y'' = (y_(i+1) - 2*y_i + y_(i-1)) / h**2

        j  = i + 1
        xj = x[j]

        c_jm1 = 1/h**2 - xj/(2*h)
        c_j   = -2/h**2 - xj
        c_jp1 = 1/h**2 + xj/(2*h)
        rhs   = 2 * xj   # this part different

        # y_(j-1)
        k = j - 1
        if 1 <= k <= N-1:
            A[i, k-1] += c_jm1
        else:
            b[i] -= c_jm1 * y0

        # y_j
        A[i, j-1] += c_j

        # y_(j+1)
        k = j + 1
        if 1 <= k <= N-1:
            A[i, k-1] += c_jp1
        else:
            b[i] -= c_jp1 * yN

        b[i] += rhs

    return A, b


#------------------------ Backward Difference -----------------------------
def backward(x, h, y0, yN):
    A = np.zeros((m, m))
    b = np.zeros(m)

    for i in range(0, m):
        # y'  ≈ (y_j - y_(j-1)) / h (backward)
        # y'' ≈ (y_j - 2*y_(j-1) + y_(j-2)) / h^2

        j  = i + 1
        xj = x[j]
        
        c_j   = 1/h**2 + (xj/h) - xj
        c_jm1 = -2/h**2 - (xj/h)
        c_jm2 = 1/h**2
        # also different
        rhs = 2*xj

        # y_(j-2)
        k = j - 2
        if 1 <= k <= N-1:
            A[i, k-1] += c_jm2
        else:
            b[i] -= c_jm2 * y0

        # y_(j-1)
        k = j - 1
        if 1 <= k <= N-1:
            A[i, k-1] += c_jm1
        else:
            b[i] -= c_jm1 * y0

        # y_j
        A[i, j-1] += c_j

        b[i] += rhs

    return A, b


print("\nExercise 1 :\n")

# Build system using 3 types differences
A_f, b_f = forward(x, h, y0, yN)

# Print matrix and RHS
print("Forward-difference matrix A:")
print(np.array2string(A_f, formatter={'float_kind': lambda z: f"{z:10.4f}"}))

print("\nRight-hand side vector b:")
print(np.array2string(b_f, formatter={'float_kind': lambda z: f"{z:10.4f}"}))

# Solve A_f*y = b_f
y_int_f = np.linalg.solve(A_f, b_f)

# Reconstruct full solution including boundaries y0, yN
y_all_f = np.zeros(N + 1)
y_all_f[0]  = y0
y_all_f[-1] = yN
y_all_f[1:-1] = y_int_f

# Print xi and y(xi)
print("\nFull solution (Forward)")
for j in range(0, N+1):
    print(f"x = {x[j]:3.1f}, y ≈ {y_all_f[j]:10.6f}")

# Central and backward for comparison
A_c, b_c = central(x, h, y0, yN)
y_int_c = np.linalg.solve(A_c, b_c)
y_all_c = np.zeros(N+1)
y_all_c[0], y_all_c[-1] = y0, yN
y_all_c[1:-1] = y_int_c

A_b, b_b = backward(x, h, y0, yN)
y_int_b = np.linalg.solve(A_b, b_b)
y_all_b = np.zeros(N+1)
y_all_b[0], y_all_b[-1] = y0, yN
y_all_b[1:-1] = y_int_b

# Extra Comparison for central and backward
print("\nBelow is extra comparison: \n")

print("Central-difference matrix A:")
print(np.array2string(A_c, formatter={'float_kind': lambda z: f"{z:10.4f}"}))

print("\nRight-hand side vector b:")
print(np.array2string(b_c, formatter={'float_kind': lambda z: f"{z:10.4f}"}))

print("\nFull solution (Central)")
for j in range(0, N+1):
    print(f"x = {x[j]:3.1f}, y ≈ {y_all_c[j]:10.6f}")

print("\nBackward-difference matrix A:")
print(np.array2string(A_b, formatter={'float_kind': lambda z: f"{z:10.4f}"}))

print("\nRight-hand side vector b:")
print(np.array2string(b_b, formatter={'float_kind': lambda z: f"{z:10.4f}"}))

print("\nFull solution (Backward)")
for j in range(0, N+1):
    print(f"x = {x[j]:3.1f}, y ≈ {y_all_b[j]:10.6f}")
    
# Table for Comparison
print("\nComparison at interior nodes (h = 0.5):")
for j in range(1, N):
    print(
        f"x = {x[j]:3.1f}\t"f"Fwd = {y_all_f[j]:10.6f},\t"f"Cent = {y_all_c[j]:10.6f},\t"f"Bwd = {y_all_b[j]:10.6f}")

# We can use RK4 in Block 2 to compute the "y_true" and make comparison.
# In conclusion, the central difference solution is much more accurate than the forward and backward.
# Forward overshoots the true curve, backward undershoots strongly.

#--------------------------------------------------------------------------------
#Exercise 2
#change h = 0.5 to h = 0.01

# Redefine the function

# Improved coeff function
def place_coeff(i_equation, j_grid, coeff, A, b, y0, yN, N):
    if 1 <= j_grid <= N-1:
        A[i_equation, j_grid - 1] += coeff
    else:
        b[i_equation] -= coeff * (y0 if j_grid == 0 else yN)


# Simplify j part (forward scheme, generic N)
def forward(x, h, y0, yN):
    N = len(x) - 1
    m = N - 1
    A = np.zeros((m, m))
    b = np.zeros(m)

    for i in range(0, m):
        # y' ≈ (y_(i+1) - y_i)/h (forward)
        # y''≈ (y_(i+2) - 2*y_(i+1) + y_i)/h**2

        xi   = x[i]
        c_i   = 1/h**2 - xi/h - xi
        c_ip1 = -2/h**2 + xi/h
        c_ip2 = 1/h**2
        rhs   = 2*xi

        place_coeff(i, i,   c_i,   A, b, y0, yN, N)
        place_coeff(i, i+1, c_ip1, A, b, y0, yN, N)
        place_coeff(i, i+2, c_ip2, A, b, y0, yN, N) #recall function

        b[i] += rhs

    return A, b

# Redefine Parameters and same logic as previous
h_fine = 0.01
x_fine = np.arange(x0, xN + h_fine/2, h_fine)
N_fine = len(x_fine) - 1

A_fine, b_fine = forward(x_fine, h_fine, y0, yN)
y_int_fine = np.linalg.solve(A_fine, b_fine)

y_fine = np.zeros(N_fine + 1)
y_fine[0]  = y0
y_fine[-1] = yN
y_fine[1:-1] = y_int_fine

print("\nExercise 2 :\n")
print(f"Number of grid points (including boundaries): {N_fine + 1}")
print(f"Step size h = {h_fine}")

# Take the point as previous easy for plotting and compare
print("\nSampled solution (forward, h = 0.01) at x = 0, 0.5, 1.0, 1.5, 2.0:")
sample_x = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
for xs in sample_x:
    j = int(round(xs / h_fine))
    print(f"x = {x_fine[j]:4.2f}, y ≈ {y_fine[j]:10.6f}")
    
#Comment:
#As the step size h decreases, the number of grid points and iterations increases.
#The forward finite difference solution becomes much closer to the high-accuracy
#RK4 benchmark obtained in Block 2. This confirms the standard convergence behaviour:
#smaller h, smaller truncation error, more accurate numerical solution.
#This naturally raises a practical question in numerical modelling:
#For a required accuracy, which method is more computationally efficient?
#Finite differences with very small h can achieve high accuracy, but the matrix
#size grows quickly. In contrast, higher-order methods like RK4 often
#achieve comparable accuracy with far fewer operations. Thus the trade-off between
#accuracy and computational cost becomes an important consideration.

#-------------------------------------------------------------------------------
# Exercise 3
# Simple graph plotting code

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

# coarse grid: markers so we can see each point clearly
plt.plot(x, y_all_f, 'o-', label='Forward, h = 0.5', color="tab:blue")
plt.plot(x, y_all_c, 'o-', label='Central, h = 0.5', color="tab:green")
plt.plot(x, y_all_b, 'o-', label='Backward, h = 0.5', color="tab:purple")

# fine grid: smooth line
plt.plot(x_fine, y_fine, '-', label='Forward, h = 0.01', color="tab:red")

plt.xlabel('x')
plt.ylabel('y(x)')
plt.title("Finite Difference Solution of $y'' + x y' - x y = 2x$\nh = 0.5 vs h = 0.01")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

print("\nGraph is plotted.")
print("\nProgram finished.")
#End of program

#Conclusion:
#The fine-grid solution (h = 0.01) provides a smooth, high-resolution reference curve.
#The coarse-grid result (h = 0.5) captures the overall trend but exhibits noticeable
#deviations at interior nodes (x = 0.5, 1.0, 1.5). In particular, the forward scheme
#(blue) shows a clear overshoot relative to the fine-grid solution.
#These differences arise from truncation error: larger step sizes lead to poorer
#approximations of y', y'' and thus larger numerical deviations.
#As expected, reducing the step size significantly improves accuracy, and the forward
#finite-difference solution converges toward the fine-grid (h = 0.01) reference curve.

#Message to Dr. Juan:
#After learning computational physics this half semester, I realized that I genuinely enjoy
#numerical methods and computational modelling. This naturally led me to develop a
#strong interest in computational astronomy, especially radio astronomy.

#I would like to understand how the numerical ideas we study—finite differences,
#matrix solvers, discretization techniques, and iterative algorithms—connect to real
#radio astronomy research workflows.

#My questions are:
# 1. Which numerical methods are most commonly used in radio astronomy?
#    (e.g., FFT-based imaging, CLEAN deconvolution, calibration algorithms,
#    FDTD/EM simulations, inverse-problem approaches, etc.)

# 2. From your perspective, what computational skills should a student develop to be
#    well-prepared for joining a research group or taking on a computational project 
#    in this field?

# 3. As I begin planning for my FYP, are there any specific research topics within
#    radio astronomy beyond the general ideas like AGN, star formation or pulsars
#    that you think are suitable, relevant and approachable from a computational angle?

# 4. Are there any recommended Python libraries or software tools I should start
#    learning (e.g., CASA, Astropy, WSClean, NumPy/SciPy-based tools)?

# Thank you, and I hope you enjoy your trip to Korea.
# Best regards,
# Tan Yee Tern