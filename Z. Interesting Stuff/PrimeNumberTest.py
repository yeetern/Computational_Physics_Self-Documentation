import math

def is_prime_and_factors(n: int):
    if n < 2:
        return False, []

    factors = set()

    limit = int(math.isqrt(n))
    for d in range(1, limit + 1):
        if n % d == 0:
            factors.add(d)
            factors.add(n // d)

    factors = sorted(factors)

    # The factors of prime number: 1 and itself
    is_prime = (factors == [1, n])
    return is_prime, factors


# User Interface
try:
    n = int(input("Enter an integer to test: "))
    prime, factors = is_prime_and_factors(n)

    if prime:
        print(f"{n} is a PRIME number.")
    else:
        print(f"{n} is NOT a prime number.")
        print("Factors:", factors)

except ValueError:
    print("Please enter a valid integer.")
