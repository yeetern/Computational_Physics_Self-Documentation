# π Digit Search Tool — Detailed Code Walkthrough (Compute → Save → Search)

This document explains **how to run** the scripts first, then goes **code-by-code** to explain how everything works under the hood.

> **Quick hack that also works (and inspired this repo):**  
> For small files (e.g., the first **1,000,000 digits**), you can open the `.txt` file in an editor and use **Ctrl+F** to check if a pattern exists.  
> I tried this and confirmed that the pattern **`23456789`** appears within the first **1,000,000** digits of π.  
>  
> That said, Ctrl+F is only a *presence check*. This repo’s scripts are built to give **reproducible results**, **exact positions**, and **scalable searching** when the file becomes large.

---

## 1) How to Use

### 1.1 Install dependency

This project is designed for **large digit counts**, so `gmpy2` is required:

```bash
pip install gmpy2
```

---

### 1.2 Compute π digits (save to file)

#### A) Save **fractional digits only** (recommended)

This outputs:

* file contains: `1415926535...` (no `"3."`, no decimal point)

```bash
python pi_compute.py --digits 1000000 --out pi_1e6.txt
```

#### B) Save `"3."+fraction` (if you want human-readable output)

This outputs:

* file contains: `3.1415926535...`

```bash
python pi_compute.py --digits 1000000 --out pi_1e6_with3.txt --with3
```

---

### 1.3 Search for a digit pattern (<= 6 digits)

#### A) Search inside fractional-only file

```bash
python pi_search.py --file pi_1e6.txt --pattern 040106
```

#### B) Search inside `"3."+fraction` file

You **must** add `--file_has_3dot` to keep indexing consistent:

```bash
python pi_search.py --file pi_1e6_with3.txt --pattern 040106 --file_has_3dot
```

---

### 1.4 Output meaning (IMPORTANT indexing convention)

This project prints:

> `fractional_position` = **1-indexed position** starting from the **first digit after the decimal point**.

Example:

* π = 3.**1**4159...
* digit `1` is at position 1
* digit `4` is at position 2

So if output is:

```
[FOUND] fractional_position = 22622
```

It means the pattern begins at the **22,622nd digit after the decimal point**.

---

### 1.5 Recommended workflow

“Don’t start with 10^7 immediately.”

1. Test pipeline:

```bash
python pi_compute.py --digits 100000 --out pi_1e5.txt
python pi_search.py  --file pi_1e5.txt --pattern 040106
```

2. Then scale up:

```bash
python pi_compute.py --digits 1000000 --out pi_1e6.txt
```

3. Only then attempt:

```bash
python pi_compute.py --digits 10000000 --out pi_1e7.txt
```

---

## 2) How `pi_compute.py` Works (Line-by-Line Explanation)

### 2.1 Imports and Dependency Guard

```python
import argparse
import time
```

* `argparse`: makes your script a CLI tool (so users can pass `--digits`, `--out`)
* `time`: measures runtime for benchmarking

```python
try:
    import gmpy2
    from gmpy2 import mpz
except ImportError as e:
    raise SystemExit(...)
```

* `gmpy2` provides:

  * big integers (`mpz`)
  * high precision floating numbers (`mpfr`)
  * fast arithmetic (internally uses GMP / MPFR)
* `mpz` is the **integer type** used heavily in binary splitting
* if missing, exit immediately with a useful message

**Why this matters:**
Computing `10^6–10^7` digits requires **fast big integer arithmetic**. Pure Python is usually too slow or memory-heavy.

---

### 2.2 Binary Splitting Function: `bs(a, b)`

```python
def bs(a: int, b: int):
```

This computes a partial sum of the Chudnovsky series **efficiently**.

#### 2.2.1 Define a constant used in the recurrence

```python
C3_OVER_24 = mpz(640320) ** 3 // 24
```

* Chudnovsky terms contain powers of `640320^(3k)`
* This constant is part of the standard binary-splitting rearrangement

#### 2.2.2 Base case: when the range has exactly one term

```python
if b - a == 1:
    k = a
```

This means: compute term `k` only.

For `k=0`:

```python
if k == 0:
    P = mpz(1)
    Q = mpz(1)
```

For `k>0`:

```python
P = mpz((6 * k - 5) * (2 * k - 1) * (6 * k - 1))
Q = mpz(k) ** 3 * C3_OVER_24
```

**Interpretation:**

* `P` and `Q` are carefully designed integer factors so that the series can be composed multiplicatively.
* This avoids repeated factorial computations directly.

Compute the linear factor:

```python
T = P * (mpz(13591409) + mpz(545140134) * k)
```

Then sign alternation:

```python
if k & 1:
    T = -T
```

Return:

```python
return P, Q, T
```

#### 2.2.3 Recursive case: split the interval into halves

```python
m = (a + b) // 2
P1, Q1, T1 = bs(a, m)
P2, Q2, T2 = bs(m, b)
```

Now combine:

```python
P = P1 * P2
Q = Q1 * Q2
T = T1 * Q2 + T2 * P1
```

Return the combined triple.

**Why binary splitting is powerful:**

* naive summation creates huge intermediate rationals repeatedly
* binary splitting builds a tree of products/sums that reduces multiplication overhead
* it improves performance especially when digits are very large

---

### 2.3 Compute π digits: `compute_pi_fractional_digits(digits)`

```python
def compute_pi_fractional_digits(digits: int) -> str:
```

Goal: return exactly `digits` digits after decimal point.

#### 2.3.1 Guard digits + set precision

```python
guard = 50
bits = int((digits + guard) * 3.3219280948873626)
gmpy2.get_context().precision = bits
```

* We need to do high precision floating operations.
* `gmpy2` uses **binary precision** (bits), not decimal digits.
* `log2(10) ≈ 3.321928...`

**Why guard digits?**

* rounding errors at the end can corrupt the last few digits
* guard digits are a safety margin, later truncated away

#### 2.3.2 Determine number of terms

```python
n_terms = digits // 14 + 2
```

Reasoning:

* one Chudnovsky term contributes ~14 digits
* +2 terms adds safety margin

#### 2.3.3 Compute the big-integer series objects

```python
t0 = time.time()
P, Q, T = bs(0, n_terms)
```

Now we have a compact representation of the sum.

#### 2.3.4 Reconstruct π

```python
sqrtC = gmpy2.sqrt(gmpy2.mpfr(10005))
pi = (gmpy2.mpfr(Q) * 426880 * sqrtC) / gmpy2.mpfr(T)
```

This corresponds to the rearranged Chudnovsky formula:

$$
\pi = \frac{Q \cdot 426880 \cdot \sqrt{10005}}{T}
$$

#### 2.3.5 Convert to decimal string and slice digits

```python
s = str(pi)
```

`s` should look like `"3.1415926535...."`

Check:

```python
if not s.startswith("3."):
    raise RuntimeError(...)
```

Extract fractional part:

```python
frac = s.split(".", 1)[1]
```

Ensure exact length:

```python
if len(frac) < digits:
    frac = frac.ljust(digits, "0")
else:
    frac = frac[:digits]
```

Finally report time:

```python
elapsed = time.time() - t0
print(f"[OK] digits={digits:,}, terms={n_terms:,}, time={elapsed:.2f}s")
```

Return digits:

```python
return frac
```

---

### 2.4 CLI entrypoint: `main()`

```python
ap = argparse.ArgumentParser()
ap.add_argument("--digits", type=int, required=True, ...)
ap.add_argument("--out", type=str, required=True, ...)
ap.add_argument("--with3", action="store_true", ...)
args = ap.parse_args()
```

* Forces users to specify digits and output file explicitly.
* `--with3` is optional.

Check:

```python
if args.digits <= 0:
    raise SystemExit("digits must be positive.")
```

Compute:

```python
frac = compute_pi_fractional_digits(args.digits)
```

Write to file:

```python
with open(args.out, "w", encoding="utf-8") as f:
    if args.with3:
        f.write("3." + frac)
    else:
        f.write(frac)
```

Report saved output:

```python
print(f"[SAVED] {args.out} ...")
```

---

## 3) How `pi_search.py` Works (Code-by-Code Explanation)

### 3.1 Streaming search: `stream_find_first(path, pattern, chunk_size)`

Goal:

* find the first occurrence of `pattern`
* without loading whole file into memory

#### 3.1.1 Overlap setup

```python
overlap = len(pattern) - 1
buf = ""
consumed = 0
```

* `buf` stores the tail of the previous chunk
* `overlap` ensures matches across boundaries are detectable

#### 3.1.2 Chunk loop

```python
with open(path, "r", encoding="utf-8") as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
```

Read 1MB at a time by default.

#### 3.1.3 Search inside `buf + chunk`

```python
data = buf + chunk
idx = data.find(pattern)
```

If found:

```python
return (consumed - len(buf)) + idx
```

This returns 0-indexed position in the entire file.

If not found:
keep tail:

```python
buf = data[-overlap:] if overlap > 0 else ""
consumed += len(chunk)
```

Return `None` if end reached.

---

### 3.2 CLI main for search

Parse args:

```python
--file
--pattern
--chunk
--file_has_3dot
```

Validate pattern:

```python
if not pattern.isdigit(): ...
if len(pattern) == 0 or len(pattern) > 6: ...
```

Run search:

```python
found0 = stream_find_first(...)
```

If not found:

```python
print("[NOT FOUND] within file range.")
```

If found:
convert to fractional digit indexing:

```python
fractional_start = 2 if args.file_has_3dot else 0
fractional_pos_1 = (found0 - fractional_start) + 1
```

* If the file begins with `"3."`, fractional digits start at index 2.
* Then we map it to 1-indexed fractional positions.

Print:

```python
print(f"[FOUND] fractional_position = ...")
print(f"raw_file_index_0 = ...")
```

---

## 4) Practical Notes / Common Pitfalls

### 4.1 Windows paths with spaces

Always quote paths:

```bash
python "Z. Interesting Stuff/pi_compute.py" --digits 100000 --out "Z. Interesting Stuff/pi_1e5.txt"
```

### 4.2 `--with3` must match `--file_has_3dot`

If you computed with `--with3`, you must search with `--file_has_3dot`.

### 4.3 Start small

Recommended scaling:

* 1e5 → confirm correctness
* 1e6 → normal usage
* 1e7 → machine dependent

---

## 5) What to Add Next (Recommended)

* Verify correctness by comparing first 50 digits with known π prefix
* Add benchmark logging:

  * digits/sec
  * memory usage
* Add multi-pattern search / regex scanning
* Add a `--count` mode (count occurrences instead of first occurrence)