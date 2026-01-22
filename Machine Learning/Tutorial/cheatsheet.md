# 🧠 SIF3012 – Tutorial 6 Cheat Sheet  
## Linear & Polynomial Regression (Machine Learning)

---

## 1. Big Picture

- Objective: use **least squares fitting** as **supervised machine learning (regression)**.
- Core task: learn a mapping  

  \[
  y = f(x)
  \]

  from data.
- Key idea: **polynomial regression is linear regression with transformed features**.

---

## 2. Physics ↔ Machine Learning Terminology

| Physics / Maths | Machine Learning |
|-----------------|------------------|
| \(x\) | Feature / Input |
| \(y\) | Target / Output |
| \(y = mx + b\) | Linear model |
| Least squares | Linear regression |
| Fit parameters | Model coefficients |
| Prediction | Inference |
| Noise | Random error |

---

## 3. Linear Regression (1D)

### Model

\[
y = a_0 + a_1 x
\]

### Assumptions

- Linear relationship
- Additive noise
- Minimize squared error

### sklearn Implementation

```python
from sklearn.linear_model import LinearRegression

x = xobs.reshape(-1, 1)   # must be 2D
y = yobs

lr = LinearRegression()
lr.fit(x, y)

a1 = lr.coef_[0]
a0 = lr.intercept_
```

## Prediction

```python
ypred = lr.predict(x_new.reshape(-1, 1))
```

## Limitation

❌ Cannot model curvature  
→ **underfitting** for nonlinear data

---

## 4. Underfitting

### Definition

Model is **too simple** to capture the data pattern.

### Example

True relation:

\[
y = 7 + 3x + x^2 + \text{noise}
\]

Linear model:

\[
y = a_0 + a_1 x
\]

Missing \(x^2\) term ⇒ systematic deviation.

## 5. Polynomial Regression (Key Concept)

### Idea

Polynomial regression = **linear regression on polynomial features**.

### Feature Mapping

\[
x \longrightarrow [x,\; x^2]
\]

### Model

\[
y = a_0 + a_1 x + a_2 x^2
\]

✔ Linear in parameters  
✔ Solved using least squares

---

## 6. Polynomial Regression (sklearn)

### Build Feature Matrix

```python
X_poly = np.column_stack((xobs, xobs**2))
y = yobs
```

Fit Model

```python
lr2 = LinearRegression()
lr2.fit(X_poly, y)
```

### Coefficients

```python
a1, a2 = lr2.coef_
a0 = lr2.intercept_
```

## 7. Prediction Methods

### Method 1: Explicit Formula

\[
\hat y = a_0 + a_1 x + a_2 x^2
\]

```python
y_pred = a0 + a1*x + a2*x**2
```

### Method 2: sklearn

```python
y_pred = lr2.predict(np
```
✔ Both methods must return the same predicted values

---

## 8. Why Polynomial Regression Works

Although the model is **nonlinear in \(x\)**, it is **linear in the coefficients**:

\[
y = a_0 + a_1 x + a_2 x^2
\]

Therefore:

- Algorithm: **Linear Regression**
- Feature space: **Polynomial**
- Solution method: **Least Squares**

This is why polynomial regression can be solved using the same linear regression algorithm.

---

## 9. Bias–Variance Intuition

| Model        | Bias | Variance |
|--------------|------|----------|
| Linear       | High | Low      |
| Quadratic    | Lower| Moderate |
| High-degree  | Low  | High     |

- Linear model → underfitting (high bias)
- Higher-degree model → risk of overfitting (high variance)

---

## 10. Plotting (Good Practice)

```python
xgrid = np.linspace(xobs.min(), xobs.max(), 100)

plt.scatter(xobs, yobs)
plt.plot(xgrid, a0 + a1*xgrid + a2*xgrid**2)
```
Always include:
- Data points
- Fitted model curve
- (Optional) comparison with linear fit

## 11. Common Mistakes (Exam Traps)

❌ Forgetting `reshape(-1, 1)` when using sklearn  
❌ Using linear regression for curved data without explaining underfitting  
❌ Calling `plt.savefig()` **after** `plt.show()`  
❌ Saying “polynomial regression is a nonlinear algorithm” (conceptually wrong)

---

## 12. One-Line Exam Answers

- **Why does linear regression fail for polynomial data?**  
  Because the hypothesis space lacks higher-order terms, causing underfitting.

- **Is polynomial regression a different algorithm?**  
  No. It is linear regression applied to polynomial feature space.

- **What does machine learning add over manual least squares?**  
  A standardized workflow for fitting, prediction, and evaluation.

---

## 13. Mental Model

> Machine learning regression  
> = physics parameter estimation  
> + feature engineering  
> + prediction