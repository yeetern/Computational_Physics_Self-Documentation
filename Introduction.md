Introduction

This repository documents the numerical methods learned in SIF3012 Computational Physics.
Each folder contains a self-contained Python implementation together with comments, mathematical background, and example outputs.
The goal is to provide a clear reference for how different numerical schemes work, when they should be used, and what trade-offs they involve.

Covered Methods

------------------------------1. Dr. Juan's Part------------------------------

------------------------------Shooting Method------------------------------
Used to solve boundary-value problems (BVPs) by converting them into initial-value problems (IVPs).
Assumption: solution behaves smoothly as the initial guess varies.
Pros: simple to implement, intuitive.
Cons: unstable for stiff or highly nonlinear systems.
Use-cases: quantum wells, beam bending equations.

-------------------------Finite Difference Method (FDM)-------------------------
Approximates derivatives using local stencils on a grid.
Assumption: solution is sufficiently smooth across the grid.
Pros: systematic, highly generalizable.
Cons: accuracy depends on grid resolution; may be unstable without proper time-stepping.
Use-cases: heat equation, wave equation, Poisson equation.

-------------------------Euler Method-------------------------
A first-order IVP solver that updates the solution using forward steps.
Assumption: small time steps keep truncation error manageable.
Pros: extremely simple and fast.
Cons: low accuracy, unstable for stiff problems.
Use-cases: quick prototyping of ODE models, teaching stability concepts.

-------------------------Discrete Fourier Transform (DFT)-------------------------
Transforms time-domain signals into frequency components.
Assumption: data is uniformly sampled.
Pros: reveals spectral content, denoising, convolution.
Cons: subject to aliasing and windowing artifacts.
Use-cases: signal processing, vibrational modes, filtering.

About This Repository:
How This Repository Is Organized?
Ans: Each numerical method has its own folder.
Python scripts are fully annotated for learning and documentation.
Examples include plots, convergence checks and runtime observations.
1. Introduction about the Method (When/How/Application)
2. Simple code that shown the Method
3. Assignment questions + Assignment Code with Notation

The repo is intended as a study companion and as a reference for future computational projects.

Purpose & Learning Outcomes
This repository helps students:
Understand how classical numerical schemes operate.
Compare their strengths, limitations, and computational cost.
Gain intuition through hands-on experimentation.
Build reusable code templates for scientific computing.