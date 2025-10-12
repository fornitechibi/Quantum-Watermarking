#!/usr/bin/env python3
"""
Diagnostic script to debug watermark reconstruction issues.
Run this when you get mismatched reconstruction results.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from watermark_lib import secret_sharing
from watermark_lib.quantum_crypto import QuantumSecretSharing

def debug_reconstruction(shares, original_secret=None):
    """Debug reconstruction discrepancies."""
    print("🔍 RECONSTRUCTION DIAGNOSTICS")
    print("=" * 50)
    print(f"Shares to reconstruct: {shares}")
    if original_secret:
        print(f"Expected result: {original_secret}")
    print("-" * 50)
    
    # Test both methods
    try:
        classical_result = secret_sharing.reconstruct_secret(shares, use_quantum=False)
        print(f"✅ Classical reconstruction: {classical_result}")
    except Exception as e:
        print(f"❌ Classical reconstruction failed: {e}")
        classical_result = None
    
    try:
        quantum_result = secret_sharing.reconstruct_secret(shares, use_quantum=True)
        print(f"✅ Quantum reconstruction: {quantum_result}")
    except Exception as e:
        print(f"❌ Quantum reconstruction failed: {e}")
        quantum_result = None
    
    # Manual Lagrange interpolation
    print("\n🧮 Manual Lagrange Interpolation:")
    secret_manual = 0.0
    print("Calculation steps:")
    
    for j, (xj, yj) in enumerate(shares):
        prod = 1.0
        basis_terms = []
        
        for m, (xm, _) in enumerate(shares):
            if m != j:
                numerator = (0 - xm)
                denominator = (xj - xm)
                term = numerator / denominator
                basis_terms.append(f"({numerator}/{denominator})")
                prod *= term
        
        contribution = yj * prod
        basis_str = " × ".join(basis_terms)
        print(f"  L_{j}(0) = {basis_str} = {prod:.6f}")
        print(f"  Term {j}: {yj} × {prod:.6f} = {contribution:.6f}")
        secret_manual += contribution
    
    manual_result = int(round(secret_manual))
    print(f"\nManual result: {secret_manual:.6f} → {manual_result}")
    
    # Analysis
    print("\n📊 ANALYSIS:")
    results = []
    if classical_result is not None:
        results.append(("Classical", classical_result))
    if quantum_result is not None:
        results.append(("Quantum", quantum_result))
    results.append(("Manual", manual_result))
    
    # Check for consistency
    unique_results = set([abs(r[1]) for r in results])
    if len(unique_results) == 1:
        print("✅ All methods agree (ignoring sign)")
    else:
        print("⚠️  Methods disagree:")
        for method, result in results:
            print(f"    {method}: {result}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if any(r[1] < 0 for r in results):
        print("⚠️  Negative result detected - this indicates precision issues")
        print("   → Use absolute value or implement better modular arithmetic")
    
    if original_secret:
        correct_results = [r for r in results if abs(r[1]) == abs(original_secret)]
        if correct_results:
            print(f"✅ Correct method(s): {[r[0] for r in correct_results]}")
        else:
            print("❌ None of the methods produced the expected result")
    
    return results

def test_common_cases():
    """Test some common problematic cases."""
    print("🧪 TESTING COMMON PROBLEMATIC CASES\n")
    
    # Test case 1: Small positive secret
    print("Test 1: Small positive secret")
    secret = 167
    shares = secret_sharing.split_secret(secret, 3, 5, use_quantum=True)
    debug_reconstruction(shares[:3], secret)
    
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Larger secret that might cause issues
    print("Test 2: Larger secret")
    secret = 2004
    shares = secret_sharing.split_secret(secret, 3, 5, use_quantum=True)
    debug_reconstruction(shares[:3], secret)
    
    print("\n" + "="*60 + "\n")
    
    # Test case 3: Manual problematic shares (example from user's error)
    print("Test 3: Simulated problematic shares")
    # These are example shares that might cause the issue
    problematic_shares = [(1, 50), (2, -200), (3, 300)]
    debug_reconstruction(problematic_shares)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_common_cases()
    else:
        print("Usage:")
        print("  python debug_reconstruction.py test    # Run test cases")
        print("  python debug_reconstruction.py         # Show usage")
        print("\nTo debug specific shares, modify the script and add your shares.")
