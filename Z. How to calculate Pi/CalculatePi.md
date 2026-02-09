# 🔢 Computing π — Algorithms, Engineering Trade-offs and Modern HPC Practice

---

## 📖 Project Motivation

I came across an idea in a science video:

> *If the digits of π behave randomly enough, then any finite piece of information could exist somewhere inside it — maybe birthdays, books or even compressed representations of the universe.*

This led to three levels of curiosity:

### Short Term

* Search my birthday / Pi Day pattern inside π digits

### Medium Term

* Understand how π is actually computed today

### Long Term

* Learn how modern HPC systems compute π to trillions of digits

---

## 🧭 Big Picture — Families of π Computation Methods

There are **four major algorithm families** historically and computationally.

| Family              | Example              | Convergence    | Modern Use              |
| ------------------- | -------------------- | -------------- | ----------------------- |
| Infinite Series     | Gregory–Leibniz      | Extremely slow | ❌ Educational only      |
| Arctan Formulas     | Machin-like          | Moderate       | ⚠️ Historical / niche   |
| Quadratic Iterative | Gauss–Legendre (AGM) | Very fast      | ⚠️ Some specialized use |
| Hyper-Fast Series   | Chudnovsky           | Extremely fast | ✅ Industry / Records    |

---

## 🧮 Method 1 — Classical Infinite Series

### Gregory–Leibniz Series


$$\pi = 4 \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1}$$


### Required Operations

* Addition / subtraction
* Division
* Alternating summation

### Limitation

Extremely slow convergence:

| Terms | Correct Digits |
| ----- | -------------- |
| 10⁶   | ~5 digits      |
| 10⁹   | ~7 digits      |

### Why Not Used

Computationally impractical for large precision.

---

## 🧮 Method 2 — Machin-Like Arctan Formulas

### Example

$$
\pi = 16\arctan\left(\frac{1}{5}\right) - 4\arctan\left(\frac{1}{239}\right)
$$

### Required Operations

* Taylor expansion of arctan
* Big integer division
* Power series accumulation

### Advantages

* Historically efficient
* Much faster than simple series

### Limitations

* Linear convergence
* Not efficient for billion-digit scale

---

## 🧮 Method 3 — Gauss–Legendre (AGM Algorithm)

### Key Idea

Uses Arithmetic–Geometric Mean iteration.

### Convergence

Digits roughly **double per iteration**.

### Required Operations

* High precision square roots
* Division
* Iterative averaging

### Advantages

* Very fast mathematically
* Elegant numerical design

### Limitations

* Hard to parallelize efficiently
* Many expensive high-precision sqrt operations

---

## 🚀 Method 4 — Chudnovsky Algorithm (Modern Standard)

### Formula

$$
\frac{1}{\pi} =
\frac{12}{640320^{3/2}}
\sum_{k=0}^{\infty}
\frac{(-1)^k (6k)! (13591409 + 545140134k)}
{(3k)! (k!)^3 (640320)^{3k}}
$$

---

### Why It Dominates Today

Each term produces ≈ **14 digits**.

| Terms  | Digits   |
| ------ | -------- |
| 100    | ~1,400   |
| 10,000 | ~140,000 |

---

### Required Operations

* Large factorial computations
* Big integer multiplication
* One high-precision square root
* Binary splitting optimization

---

### Limitation

Requires:

* Large integer arithmetic libraries
* High memory bandwidth
* Efficient multiplication algorithms

---

## 🖥 Modern HPC π Computation Pipeline

### Typical Stack

```
Chudnovsky Series
+
Binary Splitting
+
FFT-Based Multiplication
+
Massive Parallelization
```

---

### Real Software Stack

| Tool       | Purpose                        |
| ---------- | ------------------------------ |
| y-cruncher | World record π computation     |
| GMP / MPIR | Arbitrary precision integers   |
| FFTW       | Fast multiplication transforms |

---

### HPC Engineering Challenges

* Memory bandwidth bottlenecks
* Disk I/O throughput
* Cache locality optimization
* Parallel workload balancing

---

## 🐍 Python vs ⚙️ C++ — Performance Reality

---

### Python Strengths

* Fast development
* Large scientific ecosystem
* Good prototyping speed
* Works well up to ~10⁶–10⁷ digits (with gmpy2)

---

### Python Limitations

| Limitation           | Cause                   |
| -------------------- | ----------------------- |
| Interpreter overhead | Slower loop execution   |
| Memory fragmentation | Large object allocation |
| GIL                  | Limits CPU parallelism  |
| Big-int slower       | Compared to native GMP  |

---

### C++ Strengths

* Native GMP integration
* No interpreter overhead
* Fine memory control
* True multi-threading
* SIMD vectorization support

---

### Rough Performance Comparison

| Scale      | Python        | C++        |
| ---------- | ------------- | ---------- |
| 10⁶ digits | Minutes       | Seconds    |
| 10⁷ digits | Risky         | Reasonable |
| 10⁹ digits | Not practical | HPC only   |

---

## 🧠 Why Record Computations Use C++

### Reason 1 — Memory Control

Direct memory allocation and management.

### Reason 2 — CPU Vectorization

Direct access to SIMD instructions.

### Reason 3 — Parallel Execution

No GIL bottleneck.

### Reason 4 — Library Integration

GMP is written in C and optimized at low level.

---

## 🧪 When Python Is Still Ideal

For learning and personal projects:

✔ Mathematical exploration
✔ Building π digit search tools
✔ ≤ 10⁷ digit targets
✔ Rapid prototyping

Recommended stack:

```
Python + gmpy2 + Chudnovsky + Streaming Search
```

---

## 🔮 Does π Really “Contain Everything”?

If π is a **normal number**:

* Every finite digit sequence appears infinitely often

⚠ Important:
Normality of π is **not proven**.

However:
Statistically, π behaves very close to random.

---

## 🧱 Engineering Strategy (This Project)

### Phase 1

Python + gmpy2
Compute up to 10⁶–10⁷ digits
Save to file

### Phase 2

Streaming pattern search
User inputs ≤ 6 digits

### Phase 3 (Future)

C++ + GMP + FFT
Large scale computation

---

## 🌌 Philosophical Note

If π is normal, then somewhere inside π exists:

* Your birthday
* Entire books
* Potentially any finite dataset

But locating them is computationally infeasible in practice.

---

## 📌 Conclusion

Modern π computation is a fusion of:

* Number theory
* Numerical analysis
* Computer architecture
* HPC engineering

Chudnovsky + FFT dominates because it provides the best balance between:

* Convergence speed
* Parallel scalability
* Hardware efficiency

---

## 📚 Possible Future Extensions

* π digit statistical randomness tests
* Normality research
* Entropy analysis of digit distribution
* GPU acceleration experiments

---

## 🧑‍💻 Author Goal

To bridge:

* Mathematical theory
* Practical computation
* HPC engineering understanding

Through hands-on implementation.