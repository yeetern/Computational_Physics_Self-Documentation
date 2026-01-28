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
    is_prime = (factors == [1, n])
    return is_prime, factors


# ===== Main Loop =====
print("Prime Number Tester")
print("Enter an integer to test.")
print("Type 'q', 'quit', or 'exit' to stop.\n")

while True:
    user_input = input("Input number: ").strip().lower()

    if user_input in {"q", "quit", "exit"}:
        print("Program terminated by user.")
        break

    try:
        n = int(user_input)
        prime, factors = is_prime_and_factors(n)

        if prime:
            print(f"{n} is a PRIME number.\n")
        else:
            print(f"{n} is NOT a prime number.")
            print("Factors:", factors, "\n")

    except ValueError:
        print("Invalid input. Please enter an integer or 'q' to quit.\n")
