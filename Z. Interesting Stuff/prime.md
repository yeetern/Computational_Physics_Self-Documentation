# Prime Tester + Factor Lister (Python)

A simple interactive CLI program to:
1) test whether an input integer is prime, and  
2) if not prime, list all factors of the integer.

This project is designed for clarity and mathematical correctness using the classic **trial division up to √n** approach.

---

## Features

- Repeats continuously until the user quits (`q`, `quit`, `exit`)
- Handles invalid input gracefully
- For each integer `n`:
  - prints whether `n` is prime
  - if not prime, prints the full sorted list of factors

---

## How It Works (Math Idea)

If `n` is composite, then `n = a * b` for integers `a, b > 1`.
At least one of `a` or `b` must be `≤ √n`.
So we only need to test divisors up to `⌊√n⌋`.

Factors come in pairs: if `d` divides `n`, then `(d, n//d)` is a factor pair.

---

## Complexity

Let `n` be the input integer.

- **Time complexity (factor listing):** `O(√n)`  
- **Space complexity:** `O(τ(n))` for storing factors, where `τ(n)` is the number of divisors.

> Note: For a `d`-digit number, `√n` grows roughly like `10^(d/2)`.  
> This becomes slow quickly for very large integers.

---

## Usage

### Run
```bash
python prime_factors.py
```

### Example

Input number: 19391231
19391231 is NOT a prime number.
Factors: [1, 23, 89, 2047, 9473, 217879, 843097, 19391231]


### Quit

Type:
- p
- quit
- exit

---

## Limitations

This implementation uses trial division up to √n, which is reliable but can be slow for:
- very large integers (many digits)
- numbers with large prime factors (e.g., semiprimes used in RSA)

For large numbers, consider upgrading to:
- Miller–Rabin primality test (fast primality checking)
- Pollard Rho factorization (fast factor discovery)