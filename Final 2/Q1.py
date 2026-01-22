import numpy as np
import matplotlib.pyplot as plt

# Steady-state Laplace on 0<=x<=4, 0<=y<=4 with h=1
# Interior nodes: (i,j) = 1..3, 1..3  -> 9 unknowns
# 9x9 matrix
# Ordering:
# u_vec = [u11,u12,u13, u21,u22,u23, u31,u32,u33]^T
# where uij = u(x=i, y=j)


# Build A (9x9) and b (9,) from solution c
# (-4 on diagonal, +1 for neighbor couplings)
A = np.array([
    [-4,  1,  0,  1,  0,  0,  0,  0,  0],
    [ 1, -4,  1,  0,  1,  0,  0,  0,  0],
    [ 0,  1, -4,  0,  0,  1,  0,  0,  0],
    [ 1,  0,  0, -4,  1,  0,  1,  0,  0],
    [ 0,  1,  0,  1, -4,  1,  0,  1,  0],
    [ 0,  0,  1,  0,  1, -4,  0,  0,  1],
    [ 0,  0,  0,  1,  0,  0, -4,  1,  0],
    [ 0,  0,  0,  0,  1,  0,  1, -4,  1],
    [ 0,  0,  0,  0,  0,  1,  0,  1, -4],
], dtype=float)

b = np.array([
    -2,
    -2,
    -8,
    -2,
     0,   # u22: no boundary neighbors
    -6,

    -8,
    -6,
   -14,
], dtype=float)

# Solve A u = b
u_vec = np.linalg.solve(A, b)

# Put solution into full 5x5 grid (including boundaries)
U = np.zeros((5, 5), dtype=float)

# Boundary conditions:
# left:   U[0, j] = j
# right:  U[4, j] = 4 + j
# bottom: U[i, 0] = i
# top:    U[i, 4] = i + 4
for j in range(5):
    U[0, j] = j
    U[4, j] = 4 + j
for i in range(5):
    U[i, 0] = i
    U[i, 4] = i + 4

# Interior mapping (matches ordering above)
U[1, 1] = u_vec[0]
U[1, 2] = u_vec[1]
U[1, 3] = u_vec[2]
U[2, 1] = u_vec[3]
U[2, 2] = u_vec[4]
U[2, 3] = u_vec[5]
U[3, 1] = u_vec[6]
U[3, 2] = u_vec[7]
U[3, 3] = u_vec[8]

# Print results
np.set_printoptions(precision=6, suppress=True)
print("u_vec = [u11,u12,u13,u21,u22,u23,u31,u32,u33]^T")
print(u_vec)
print("\nFull grid U (x index along rows, y index along columns):")
print(U)

# Plot
plt.figure(figsize=(5,4))
plt.imshow(U.T, origin="lower", interpolation="nearest")
plt.colorbar(label="Temperature u")
plt.title("Steady-state Laplace solution (5x5 grid, h=1)")
plt.xlabel("x index (i)")
plt.ylabel("y index (j)")
plt.tight_layout()
plt.savefig('output.png')
plt.show()
