from typing import List
import random
from sympy import symbols

def polynom(x, coefficients):
    res = 0
    for i, c in enumerate(coefficients):
        res += c * (x**i)
    return res

def split_secret(secret: int, threshold: int, num_shares: int) -> List[tuple]:
    if threshold > num_shares:
        raise ValueError("Threshold must be <= num_shares")
    coeffs = [secret] + [random.randint(0, 1000) for _ in range(threshold -1)]
    shares = []
    for i in range(1, num_shares + 1):
        shares.append((i, polynom(i, coeffs)))
    return shares

def reconstruct_secret(shares: List[tuple]) -> int:
    if len(shares) < 2:
        raise ValueError("At least two shares are required")

    xs = [s[0] for s in shares]
    if len(xs) != len(set(xs)):
        raise ValueError("Duplicate share indices")

    x = symbols('x')
    secret = 0
    for j, (xj, yj) in enumerate(shares):
        prod = 1
        for m, (xm, _) in enumerate(shares):
            if m != j:
                denom = (xj - xm)
                if denom == 0:
                    raise ValueError("Duplicate share indices cause division by zero")
                prod *= (0 - xm) / denom
        secret += yj * prod
    return int(round(secret))
