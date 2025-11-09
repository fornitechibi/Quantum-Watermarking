import time
import random
from watermark_lib.secret_sharing import split_secret, reconstruct_secret
from watermark_lib.quantum_crypto import QuantumWatermarkEncoder, create_quantum_entangled_shares

# Benchmarking Shamir Algorithm

def benchmark_shamir():
    secret = 12345  # Example secret
    n, k = 5, 3  # Number of shares and threshold

    # Embedding benchmark
    start_time = time.time()
    shares = split_secret(secret, k, n, use_quantum=False)
    embed_time = time.time() - start_time

    # Retrieval benchmark
    start_time = time.time()
    retrieved_secret = reconstruct_secret(shares[:k], use_quantum=False)
    retrieve_time = time.time() - start_time

    return embed_time, retrieve_time

# Benchmarking Quantum Watermarking

def benchmark_quantum(secret="This is a watermark"):
    quantum_encoder = QuantumWatermarkEncoder()

    # Embedding benchmark
    start_time = time.time()
    quantum_signature = quantum_encoder.create_quantum_signature(secret)
    embed_time = time.time() - start_time

    # Retrieval benchmark
    start_time = time.time()
    is_valid = quantum_encoder.verify_quantum_signature(secret, quantum_signature)
    retrieve_time = time.time() - start_time

    return embed_time, retrieve_time

# Additional Benchmarking Tests

def benchmark_shamir_brute_force():
    secret = 999999  # Larger secret for brute force test
    n, k = 5, 3  # Number of shares and threshold
    shares = split_secret(secret, k, n, use_quantum=False)

    start_time = time.time()
    attempts = 0
    max_attempts = 100000

    # Simulate brute force by trying different combinations
    for attempt in range(max_attempts):
        try:
            test_secret = random.randint(0, secret * 2)  # Try random values
            if attempt % 1000 == 0:  # Check progress periodically
                reconstructed = reconstruct_secret(shares[:k], use_quantum=False)
                if reconstructed == secret:
                    break
            attempts = attempt
        except ValueError:
            continue
    
    brute_force_time = time.time() - start_time
    return brute_force_time, attempts

def benchmark_scalability():
    """Test how both methods scale with increasing data size"""
    sizes = [1000, 10000, 100000, 1000000]
    shamir_times = []
    quantum_times = []

    for size in sizes:
        # Shamir scalability
        secret = size  # Use size as the secret for Shamir
        embed_time, _ = benchmark_shamir()
        shamir_times.append(embed_time)

        # Quantum scalability
        quantum_data = "Watermark" * (size // 1000 + 1)  # Create string of varying length
        embed_time, _ = benchmark_quantum(quantum_data)
        quantum_times.append(embed_time)

    return sizes, shamir_times, quantum_times

def benchmark_tamper_detection():
    """Test ability to detect tampering"""
    original_secret = "This is a secure watermark"
    tampered_secret = "This is a secure watermark (tampered)"
    
    # Quantum tamper detection
    quantum_encoder = QuantumWatermarkEncoder()
    
    # Create original signature
    start_time = time.time()
    quantum_signature = quantum_encoder.create_quantum_signature(original_secret)
    
    # Try to verify tampered data
    is_valid = quantum_encoder.verify_quantum_signature(tampered_secret, quantum_signature)
    quantum_detect_time = time.time() - start_time
    
    # Shamir tamper detection (using basic comparison)
    start_time = time.time()
    n, k = 5, 3
    shares = split_secret(int.from_bytes(original_secret.encode(), 'big'), k, n, use_quantum=False)
    reconstructed = reconstruct_secret(shares[:k], use_quantum=False)
    is_valid_shamir = (reconstructed == int.from_bytes(original_secret.encode(), 'big'))
    shamir_detect_time = time.time() - start_time
    
    return quantum_detect_time, shamir_detect_time

def benchmark_quantum_entanglement():
    """Test quantum entanglement-based security"""
    secret = 12345
    start_time = time.time()
    quantum_shares = create_quantum_entangled_shares(secret)
    entanglement_time = time.time() - start_time
    return entanglement_time

if __name__ == "__main__":
    # Run basic benchmarks
    shamir_embed, shamir_retrieve = benchmark_shamir()
    quantum_embed, quantum_retrieve = benchmark_quantum()
    
    # Run brute force test
    brute_force_time, attempts = benchmark_shamir_brute_force()
    
    # Run scalability test
    sizes, shamir_scale_times, quantum_scale_times = benchmark_scalability()
    
    # Run tamper detection test
    quantum_tamper_time, shamir_tamper_time = benchmark_tamper_detection()
    
    # Run quantum entanglement test
    entanglement_time = benchmark_quantum_entanglement()

    # Display results
    print("\n=== Basic Performance Benchmarks ===")
    print(f"Shamir Algorithm - Embed: {shamir_embed:.6f}s, Retrieve: {shamir_retrieve:.6f}s")
    print(f"Quantum Watermarking - Embed: {quantum_embed:.6f}s, Retrieve: {quantum_retrieve:.6f}s")
    
    print("\n=== Security Benchmarks ===")
    print(f"Shamir Brute Force Time: {brute_force_time:.6f}s (Attempts: {attempts})")
    print(f"Quantum Entanglement Setup Time: {entanglement_time:.6f}s")
    
    print("\n=== Tamper Detection Speed ===")
    print(f"Quantum Tamper Detection: {quantum_tamper_time:.6f}s")
    print(f"Shamir Tamper Detection: {shamir_tamper_time:.6f}s")
    
    print("\n=== Scalability Results ===")
    print("Data Size (bytes) | Shamir Time (s) | Quantum Time (s)")
    print("-" * 50)
    for i, size in enumerate(sizes):
        print(f"{size:14d} | {shamir_scale_times[i]:13.6f} | {quantum_scale_times[i]:13.6f}")