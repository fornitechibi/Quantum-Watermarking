import matplotlib.pyplot as plt
import numpy as np
from bechmark.benchmark_shamir_vs_quantum import *

def plot_basic_performance():
    # Run basic benchmarks
    shamir_embed, shamir_retrieve = benchmark_shamir()
    quantum_embed, quantum_retrieve = benchmark_quantum()

    # Create grouped bar chart
    labels = ['Embedding Time', 'Retrieval Time']
    shamir_times = [shamir_embed, shamir_retrieve]
    quantum_times = [quantum_embed, quantum_retrieve]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, shamir_times, width, label='Shamir Algorithm')
    rects2 = ax.bar(x + width/2, quantum_times, width, label='Quantum Watermarking')

    ax.set_ylabel('Time (seconds)')
    ax.set_title('Performance Comparison: Shamir vs Quantum Watermarking')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.tight_layout()
    plt.savefig('benchmark_basic_performance.png')
    plt.close()

def plot_scalability():
    # Run scalability test
    sizes, shamir_times, quantum_times = benchmark_scalability()

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, shamir_times, 'o-', label='Shamir Algorithm')
    plt.plot(sizes, quantum_times, 's-', label='Quantum Watermarking')
    
    plt.xlabel('Data Size')
    plt.ylabel('Processing Time (seconds)')
    plt.title('Scalability Comparison')
    plt.legend()
    plt.xscale('log')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('benchmark_scalability.png')
    plt.close()

def plot_security_comparison():
    # Run security benchmarks
    brute_force_time, attempts = benchmark_shamir_brute_force()
    quantum_tamper_time, shamir_tamper_time = benchmark_tamper_detection()
    entanglement_time = benchmark_quantum_entanglement()

    # Create bar chart for security metrics
    labels = ['Tamper Detection', 'Security Setup']
    shamir_times = [shamir_tamper_time, brute_force_time]
    quantum_times = [quantum_tamper_time, entanglement_time]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, shamir_times, width, label='Shamir Algorithm')
    rects2 = ax.bar(x + width/2, quantum_times, width, label='Quantum Watermarking')

    ax.set_ylabel('Time (seconds)')
    ax.set_title('Security Metrics Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.tight_layout()
    plt.savefig('benchmark_security.png')
    plt.close()

if __name__ == "__main__":
    # Generate all plots
    plot_basic_performance()
    plot_scalability()
    plot_security_comparison()
    
    print("Benchmark plots have been generated:")
    print("1. benchmark_basic_performance.png")
    print("2. benchmark_scalability.png")
    print("3. benchmark_security.png")