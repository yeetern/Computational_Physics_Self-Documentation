"""
Compute pi to N digits after the decimal point using the Chudnovsky formula
with binary splitting, then save the fractional digits to a file.

Recommended:
  pip install gmpy2

Usage:
  python pi_compute.py --digits 1000000 --out pi_1e6.txt
  python pi_compute.py --digits 1000000 --out pi_1e6_with3.txt --with3

Notes:
- Default output contains ONLY digits after decimal point.
- Indexing for search: position 1 = first digit after decimal point.
"""

import argparse
import time

try:
    import gmpy2
    from gmpy2 import mpz
except ImportError as e:
    raise SystemExit(
        "Missing dependency: gmpy2.\n"
        "Install with: pip install gmpy2\n"
        "For 1e6+ digits, pure Python is not recommended."
    ) from e


def bs(a: int, b: int):
    """
    Binary splitting for Chudnovsky series.

    Returns (P, Q, T) such that:
      sum_{k=a}^{b-1} term(k) = T / Q  (up to a shared factor)
    """
    C3_OVER_24 = mpz(640320) ** 3 // 24  # 640320^3 / 24

    if b - a == 1:
        k = a
        if k == 0:
            P = mpz(1)
            Q = mpz(1)
        else:
            P = mpz((6 * k - 5) * (2 * k - 1) * (6 * k - 1))
            Q = mpz(k) ** 3 * C3_OVER_24

        T = P * (mpz(13591409) + mpz(545140134) * k)
        if k & 1:
            T = -T
        return P, Q, T

    m = (a + b) // 2
    P1, Q1, T1 = bs(a, m)
    P2, Q2, T2 = bs(m, b)

    P = P1 * P2
    Q = Q1 * Q2
    T = T1 * Q2 + T2 * P1
    return P, Q, T


def compute_pi_fractional_digits(digits: int) -> str:
    """
    Compute pi and return exactly `digits` digits after the decimal point as a string.
    """
    # Guard digits protect against rounding/truncation at the tail.
    guard = 50
    # bits ≈ decimal_digits * log2(10)
    bits = int((digits + guard) * 3.3219280948873626)
    gmpy2.get_context().precision = bits

    # Each term contributes ~14 digits
    n_terms = digits // 14 + 2

    t0 = time.time()
    P, Q, T = bs(0, n_terms)

    sqrtC = gmpy2.sqrt(gmpy2.mpfr(10005))
    pi = (gmpy2.mpfr(Q) * 426880 * sqrtC) / gmpy2.mpfr(T)

    # Convert to decimal string with enough digits (includes "3.")
    s = str(pi)
    elapsed = time.time() - t0

    if not s.startswith("3."):
        raise RuntimeError(f"Unexpected pi format: {s[:20]}...")

    frac = s.split(".", 1)[1]
    if len(frac) < digits:
        frac = frac.ljust(digits, "0")
    else:
        frac = frac[:digits]

    print(f"[OK] digits={digits:,}, terms={n_terms:,}, time={elapsed:.2f}s")
    return frac


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--digits", type=int, required=True,
                    help="Number of digits after decimal point (e.g. 1000000, 10000000)")
    ap.add_argument("--out", type=str, required=True, help="Output file path")
    ap.add_argument("--with3", action="store_true",
                    help='Write "3."+digits instead of digits only')
    args = ap.parse_args()

    if args.digits <= 0:
        raise SystemExit("digits must be positive.")

    frac = compute_pi_fractional_digits(args.digits)

    with open(args.out, "w", encoding="utf-8") as f:
        if args.with3:
            f.write("3." + frac)
        else:
            f.write(frac)

    print(f"[SAVED] {args.out} (length={len(frac) + (2 if args.with3 else 0):,} chars)")


if __name__ == "__main__":
    main()
