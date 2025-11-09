"""
plot_additional_benchmark.py
Author: Shibi Kishore N
Purpose: Generate extended benchmark figures for
         "Enhancing Digital Watermarking Security:
          A Comparative Analysis of Classical Shamir’s Secret Sharing
          and Quantum-Enhanced Methods"
"""

import math
import random
import numpy as np
import matplotlib.pyplot as plt

# Import your existing benchmark utilities
from bechmark.benchmark_shamir_vs_quantum import (
    split_secret,
    reconstruct_secret,
    QuantumWatermarkEncoder,
)


# ==============================================================
# Utility Functions
# ==============================================================

def shannon_entropy(byte_seq):
    """Compute Shannon entropy (bits/byte)."""
    if not byte_seq:
        return 0.0
    counts = {}
    for b in byte_seq:
        counts[b] = counts.get(b, 0) + 1
    n = len(byte_seq)
    probs = [c / n for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)


def corrupt_bytes(data: bytes, flip_prob: float, rng: random.Random) -> bytes:
    """Flip each bit in a bytearray with probability flip_prob."""
    out = bytearray(data)
    for i in range(len(out)):
        byte = out[i]
        for bit in range(8):
            if rng.random() < flip_prob:
                byte ^= (1 << bit)
        out[i] = byte
    return bytes(out)


def corrupt_string(s: str, char_flip_prob: float, rng: random.Random) -> str:
    """Apply character-level corruption for quantum signature simulation."""
    if not s:
        return s
    chars = list(s)
    for i, ch in enumerate(chars):
        if rng.random() < char_flip_prob:
            chars[i] = chr(rng.randint(33, 126))  # random printable ASCII
    return "".join(chars)


def int_byte_len(i: int) -> int:
    """Return minimum bytes required to represent integer i."""
    return max(1, (i.bit_length() + 7) // 8)


def to_fixed_bytes(i: int, width: int) -> bytes:
    """Convert int to fixed-length bytes, zero-padded to width."""
    b = i.to_bytes(int_byte_len(i), "big", signed=False)
    return b.rjust(width, b"\x00")


# ==============================================================
# 1) Entropy Preservation Benchmark
# ==============================================================

def plot_entropy_preservation(
    payload_bytes: int = 4096,
    n: int = 5,
    k: int = 3,
    seed: int = 42,
    out_path: str = "benchmark_entropy_preservation.png",
):
    """
    Compares entropy of Original Data vs Classical (SSS) vs Quantum representations.
    """
    rng = random.Random(seed)

    # --- Original Data
    original = bytes(rng.getrandbits(8) for _ in range(payload_bytes))
    H_original = shannon_entropy(original)

    # --- Classical (SSS) Representation
    secret_int = int.from_bytes(original[: min(32, payload_bytes)], "big", signed=False)
    shares = split_secret(secret_int, k, n, use_quantum=False)

    shares_bytes = []
    for (x, y) in shares:
        xb = x.to_bytes(2, "big", signed=False)
        yb = y.to_bytes(int_byte_len(y), "big", signed=False)
        shares_bytes.append(xb + yb)
    classical_blob = b"".join(shares_bytes)
    H_classical = shannon_entropy(classical_blob)

    # --- Quantum Representation
    enc = QuantumWatermarkEncoder()
    q_sig = enc.create_quantum_signature(original.hex())
    q_bytes = q_sig.encode("utf-8", errors="ignore")
    H_quantum = shannon_entropy(q_bytes)

    # --- Plot
    labels = ["Original", "Classical (SSS)", "Quantum"]
    entropies = [H_original, H_classical, H_quantum]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, entropies, color=["#5DADE2", "#58D68D", "#AF7AC5"])
    ax.set_ylabel("Shannon Entropy (bits/byte)")
    ax.set_title("Entropy Preservation: Original vs Classical vs Quantum")
    ax.set_ylim(0, 8)
    for bar, val in zip(bars, entropies):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.05, f"{val:.2f}",
                ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[OK] Saved entropy plot → {out_path}")


# ==============================================================
# 2) Noise / Decoherence Resilience Benchmark
# ==============================================================

def plot_noise_resilience(
    error_rates=(0.0, 0.005, 0.01, 0.02, 0.05, 0.1),
    trials_per_rate: int = 100,
    seed: int = 1337,
    out_path: str = "benchmark_noise_resilience.png",
):
    """
    Simulates noise or decoherence by corrupting data representations
    and measuring verification/reconstruction success.
    """
    rng = random.Random(seed)
    enc = QuantumWatermarkEncoder()

    payload = "This is a secure watermark for noise-resilience testing"
    quantum_acc, classical_acc = [], []

    for p in error_rates:
        # --- Quantum trials ---
        q_success = 0
        for _ in range(trials_per_rate):
            sig = enc.create_quantum_signature(payload)
            noisy_sig = corrupt_string(sig, char_flip_prob=p, rng=rng)
            if enc.verify_quantum_signature(payload, noisy_sig):
                q_success += 1
        quantum_acc.append(q_success / trials_per_rate)

        # --- Classical trials ---
        c_success = 0
        secret_int = int.from_bytes(payload.encode("utf-8"), "big", signed=False)
        n, k = 5, 3
        shares = split_secret(secret_int, k, n, use_quantum=False)

        # Compute safe fixed byte-widths for each run
        x_width = max(int_byte_len(x) for x, _ in shares)
        y_width = max(int_byte_len(y) for _, y in shares)

        for _ in range(trials_per_rate):
            noisy_shares = []
            for (x, y) in shares:
                xb = to_fixed_bytes(x, x_width)
                yb = to_fixed_bytes(y, y_width)

                xb_noisy = corrupt_bytes(xb, p, rng)
                yb_noisy = corrupt_bytes(yb, p, rng)

                x_noisy = int.from_bytes(xb_noisy, "big", signed=False)
                y_noisy = int.from_bytes(yb_noisy, "big", signed=False)
                noisy_shares.append((x_noisy, y_noisy))

            try:
                recovered = reconstruct_secret(noisy_shares[:k], use_quantum=False)
                if recovered == secret_int:
                    c_success += 1
            except Exception:
                pass

        classical_acc.append(c_success / trials_per_rate)

    # --- Plot
    x = np.array(error_rates)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, classical_acc, "o-", label="Classical (SSS) Verification Accuracy", linewidth=2)
    ax.plot(x, quantum_acc, "s-", label="Quantum Verification Accuracy", linewidth=2)
    ax.set_xlabel("Bit/Char Error Rate (probability)")
    ax.set_ylabel("Verification Accuracy")
    ax.set_title("Noise/Decoherence Resilience: Accuracy vs. Error Rate")
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[OK] Saved noise/decoherence plot → {out_path}")


# ==============================================================
# Main Execution
# ==============================================================

if __name__ == "__main__":
    plot_entropy_preservation()
    plot_noise_resilience()
    print("\nAll extended benchmark plots generated successfully:")
    print("1. benchmark_entropy_preservation.png")
    print("2. benchmark_noise_resilience.png")
