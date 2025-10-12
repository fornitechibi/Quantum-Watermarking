#!/usr/bin/env python3
"""
Quick test to verify the signature verification fix
"""

from PIL import Image
import numpy as np
from watermark_lib.embedder import embed_quantum_enhanced_watermark
from watermark_lib.extractor import extract_quantum_enhanced_watermark

def test_signature_verification():
    """Test that signature verification works correctly with quantum enhancement"""
    
    # Create a test image
    test_image = Image.new('L', (100, 100), 128)
    
    # Test secret
    secret = 42
    bit_length = 8
    
    print("🔬 Testing Quantum-Enhanced Watermarking with Signature Verification")
    print(f"Original secret: {secret}")
    print(f"Bit length: {bit_length}")
    
    # Embed with quantum enhancement
    watermarked_image, quantum_signature, quantum_key = embed_quantum_enhanced_watermark(
        test_image, secret, bit_length
    )
    
    print(f"Quantum key: {quantum_key}")
    print(f"Quantum signature: {quantum_signature[:32]}... (truncated)")
    
    # Extract with quantum enhancement
    extracted_secret, is_verified = extract_quantum_enhanced_watermark(
        watermarked_image, bit_length, quantum_signature, quantum_key
    )
    
    print(f"Extracted secret: {extracted_secret}")
    print(f"Signature verified: {'✓ YES' if is_verified else '✗ NO'}")
    
    # Verify correctness
    success = (extracted_secret == secret) and is_verified
    print(f"\n🎯 Test Result: {'✅ PASSED' if success else '❌ FAILED'}")
    
    if not success:
        print(f"Expected: secret={secret}, verified=True")
        print(f"Got: secret={extracted_secret}, verified={is_verified}")
    
    return success

if __name__ == "__main__":
    test_signature_verification()
