from typing import List
import random
from sympy import symbols
from .quantum_crypto import QuantumSecretSharing, QuantumKeyGenerator

def polynom(x, coefficients):
    res = 0
    for i, c in enumerate(coefficients):
        res += c * (x**i)
    return res

def split_secret(secret: int, threshold: int, num_shares: int, use_quantum: bool = True) -> List[tuple]:
    """
    Split secret using classical or quantum-enhanced Shamir's Secret Sharing.
    
    Args:
        secret: Secret integer to split
        threshold: Minimum shares needed for reconstruction
        num_shares: Total number of shares to generate
        use_quantum: Whether to use quantum-enhanced sharing
        
    Returns:
        List of (x, y) coordinate pairs representing shares
    """
    if threshold > num_shares:
        raise ValueError("Threshold must be <= num_shares")
    
    if use_quantum:
        # Use quantum-enhanced secret sharing
        quantum_ss = QuantumSecretSharing()
        return quantum_ss.quantum_split_secret(secret, threshold, num_shares)
    else:
        # Classical implementation
        coeffs = [secret] + [random.randint(0, 1000) for _ in range(threshold - 1)]
        shares = []
        for i in range(1, num_shares + 1):
            shares.append((i, polynom(i, coeffs)))
        return shares

def reconstruct_secret(shares: List[tuple], use_quantum: bool = True) -> int:
    """
    Reconstruct secret from shares using classical or quantum-enhanced methods.
    
    Args:
        shares: List of (x, y) coordinate pairs
        use_quantum: Whether to use quantum-enhanced reconstruction
        
    Returns:
        Reconstructed secret integer
    """
    if len(shares) < 2:
        raise ValueError("At least two shares are required")

    xs = [s[0] for s in shares]
    if len(xs) != len(set(xs)):
        raise ValueError("Duplicate share indices")

    if use_quantum:
        # Use quantum-enhanced reconstruction
        quantum_ss = QuantumSecretSharing()
        return quantum_ss.lagrange_interpolation(shares)
    else:
        # Classical implementation
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


def generate_quantum_key(bit_length: int) -> int:
    """
    Generate a quantum random key for additional security.
    
    Args:
        bit_length: Length of the key in bits
        
    Returns:
        Quantum-generated random key
    """
    qrng = QuantumKeyGenerator()
    return qrng.generate_quantum_key(bit_length)
