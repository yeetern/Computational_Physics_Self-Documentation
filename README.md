# 🧮 Computational Physics — Numerical Methods & Simulations

This repository is a growing collection of numerical methods, simulations, and computational tools developed during and beyond SIF3012 – Computational Physics.

All methods are implemented in Python, with emphasis on:
- physical intuition
- numerical stability & accuracy
- clean, reusable code
- research-oriented workflows

The repository serves both as a learning reference and a technical portfolio for computational physics, data analysis, and simulation-based research.

---

## 📂 Repository Structure & Topics
### 1. Ordinary Differential Equations (ODEs)

Folders:
- 1. Euler Method
- 2. Shooting Method

Covered methods:
- Euler method (stability, truncation error)
- Shooting method for boundary-value problems
- Sensitivity to initial guesses
- Convergence and failure modes

Typical applications:
- Classical mechanics
- Quantum wells
- Beam equations
- Nonlinear ODE systems

---

### 2. Boundary-Value Problems & Linear Systems

Folders:
- 3. Finite Difference Method
- How to solve Ax=b matrix

Covered techniques:
- Finite difference stencils (forward / backward / central)
- Matrix formulation of differential equations
- Solving linear systems via LU, Gauss elimination
- Error analysis and grid dependence

Applications:
- Poisson equation
- Diffusion problems
- Electrostatics and steady-state systems

---

### 3. Partial Differential Equations (PDEs)

Folder:
- pde
- Topics include:
- Discretization of PDEs
- Spatial–temporal grids
- Stability considerations
- Physical interpretation of numerical solutions

---

### 4. Fourier Analysis & Signal Processing

Folder:
- 4. Discrete Fourier Transform

Covered concepts:
- Discrete Fourier Transform (DFT)
- Fast Fourier Transform (FFT)
- Frequency-domain filtering
- Aliasing and sampling effects

Applications:
- Periodic noise removal
- Spectral analysis
- Image and signal processing

---

### 5. Probability & Monte Carlo Methods

Folder:
- Probability (Monte Carlo)

Includes:
- Random sampling techniques
- Monte Carlo estimation
- Probabilistic interpretation of numerical results
- Links between statistics and physical systems

---

### 6. Machine Learning (Foundations & Tutorials)

Folder:
- Machine Learning/Tutorial

Focus:
- Introductory ML concepts
- Data-driven modeling
- Foundations for future physics–ML integration

---

### 7. Self-Learning, Experiments & Exploration

Folders:
- Z. Interesting Stuff
- Z. Self_Learning(Play)/Simulate

Purpose:
- Open-ended simulations
- Numerical experiments
- Exploratory coding beyond syllabus constraints

---

### 8. Final & Consolidated Work

Folders:
- Final
- Final 2

Contains polished scripts, assessments, and finalized implementations consolidating multiple numerical methods.

## 🎯 Purpose of This Repository

This repository is designed to:
- Document computational physics training
- Serve as a reference for future students
- Provide reusable simulation templates
- Demonstrate numerical & coding competence for:
    - research internships
    - final-year projects
    - computational research roles

## 🚀 How to Use

Clone the repository:

```bash
git clone <repo-url>
```

Navigate to any topic folder, then run:

```bash
python <script_name>.py
```


Each script typically includes:
- Mathematical background
- Numerical logic and assumptions
- Well-commented Python implementation
- Visualization (when applicable)

## 🛠 Dependencies

Install required packages:
```bash
pip install numpy matplotlib
```

(Some sections may later include scipy, pandas, or ML libraries.)

## 📘 Learning Outcomes

By working through this repository, you will learn how to:
- Translate physical models into numerical algorithms
- Evaluate accuracy, stability, and computational cost
- Diagnose numerical failure modes
- Build intuition for choosing the right method
- Develop research-ready simulation pipelines

## 📄 License
Released under the MIT License.
Free to use, modify, and adapt for academic or personal projects.

## 🤝 Contributions

Suggestions, improvements, or extensions are welcome.
Feel free to open an issue or submit a pull request.