🧮 Computational Physics — Numerical Methods Collection

This repository documents the key numerical methods learned in SIF3012 Computational Physics.
Each method is implemented in Python with clear explanations, comments, and example outputs.
The aim is to build a concise but rigorous reference for solving differential equations, boundary-value problems, and signal-processing tasks commonly encountered in physics.

📂 Contents
1. Shooting Method

Solves boundary-value problems by converting them into a sequence of initial-value problems.

Useful for: quantum well problems, beam equations, nonlinear ODEs.

Notes include convergence behaviour, sensitivity to initial guesses, and stability issues.

2. Finite Difference Method (FDM)

Approximates derivatives using discrete stencils on a spatial grid.

Used for: heat equation, wave equation, Poisson equation, diffusion problems.

Includes forward/central/backward schemes, stability comments, and example plots.

3. Euler Method

First-order ODE solver that updates solutions via forward stepping.

Ideal for teaching stability, truncation error, and numerical divergence.

Scripts also compare Euler with higher-order methods.

4. Discrete Fourier Transform (DFT)

Converts time-domain signals into frequency components.

Applications: noise filtering, signal analysis, spectral interpretation.

Includes sampling considerations, aliasing, and FFT implementation.

🎯 Purpose of This Repository

This repository is created for:

Documentation of course content and coding practice.

Learning reference for future students taking computational physics.

Reusable templates for numerical simulations in research projects.

Demonstrating numerical skills in a clean, well-organized GitHub portfolio.

🚀 How to Use

Clone the repository:

git clone <repo-url>


Navigate to any folder (e.g., DFT, Euler Method).

Run the corresponding Python script:

python Block1_23006131.py


Each script contains:

Mathematical background

Step-by-step implementation

Annotated code

Generated plots (when applicable)

🛠 Dependencies

Install required libraries using:

pip install numpy matplotlib

📘 Learning Outcomes

By exploring this repository, you will:

Understand how major numerical methods work.

Compare accuracy, stability, and computational cost.

Learn how to translate mathematical models into real simulations.

Build intuition for when each method should be used.

📄 License

This project is released under the MIT License.
Feel free to fork, modify, and use the code for academic or personal projects.

🤝 Contributions

Suggestions, improvements, or additional numerical methods are welcome.
You may open an issue or submit a pull request.