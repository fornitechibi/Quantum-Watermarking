#!/usr/bin/env python3
"""
Test script for quantum-enhanced watermarking system.
Tests the integration of Qiskit quantum computing with the watermarking application.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from watermark_lib.quantum_crypto import (
    QuantumKeyGenerator, 
    QuantumSecretSharing, 
    QuantumWatermarkEncoder,
    create_quantum_entangled_shares
)
from watermark_lib import secret_sharing, embedder, extractor
from PIL import Image
import numpy as np

def test_quantum_key_generation():
    """Test quantum random key generation."""
    print("🔑 Testing Quantum Key Generation...")
    
    qrng = QuantumKeyGenerator()
    
    # Generate quantum random bits
    bits = qrng.generate_quantum_random_bits(8)
    print(f"Generated quantum bits: {bits}")
    assert len(bits) == 8
    assert all(bit in '01' for bit in bits)
    
    # Generate quantum key
    key = qrng.generate_quantum_key(16)
    print(f"Generated quantum key: {key} (0x{key:x})")
    assert isinstance(key, int)
    assert key >= 0
    
    print("✅ Quantum key generation test passed!\n")

def test_quantum_secret_sharing():
    """Test quantum-enhanced secret sharing."""
    print("🔐 Testing Quantum Secret Sharing...")
    
    secret = 12345
    threshold = 3
    num_shares = 5
    
    # Test quantum-enhanced sharing
    shares = secret_sharing.split_secret(secret, threshold, num_shares, use_quantum=True)
    print(f"Generated {len(shares)} quantum shares for secret {secret}")
    
    # Test reconstruction
    reconstructed = secret_sharing.reconstruct_secret(shares[:threshold], use_quantum=True)
    print(f"Reconstructed secret: {reconstructed}")
    
    assert reconstructed == secret, f"Expected {secret}, got {reconstructed}"
    print("✅ Quantum secret sharing test passed!\n")

def test_quantum_watermark_encoder():
    """Test quantum watermark encoding and verification."""
    print("🎯 Testing Quantum Watermark Encoder...")
    
    encoder = QuantumWatermarkEncoder()
    
    # Test quantum signature
    watermark_data = "12345:16"
    signature = encoder.create_quantum_signature(watermark_data)
    print(f"Generated quantum signature: {signature[:32]}...")
    
    # Test verification
    is_valid = encoder.verify_quantum_signature(watermark_data, signature)
    print(f"Signature verification: {is_valid}")
    assert is_valid, "Quantum signature verification failed"
    
    # Test with tampered data
    tampered_data = "54321:16"
    is_valid_tampered = encoder.verify_quantum_signature(tampered_data, signature)
    print(f"Tampered data verification: {is_valid_tampered}")
    assert not is_valid_tampered, "Should reject tampered data"
    
    print("✅ Quantum watermark encoder test passed!\n")

def test_quantum_entangled_shares():
    """Test quantum entangled share generation."""
    print("⚛️  Testing Quantum Entangled Shares...")
    
    secret = 255  # 8-bit secret
    quantum_shares = create_quantum_entangled_shares(secret, 8)
    
    print(f"Generated {len(quantum_shares)} quantum entangled shares:")
    for i, share in enumerate(quantum_shares):
        print(f"  Share {i+1}: {share}")
    
    assert len(quantum_shares) == 3
    assert all(len(share) == 8 for share in quantum_shares)
    assert all(all(bit in '01' for bit in share) for share in quantum_shares)
    
    print("✅ Quantum entangled shares test passed!\n")

def test_full_quantum_watermarking():
    """Test complete quantum watermarking workflow."""
    print("🖼️  Testing Full Quantum Watermarking Workflow...")
    
    # Create a test image
    test_image = Image.new('L', (100, 100), 128)  # Gray image
    secret = 42
    bit_length = secret.bit_length()
    
    # Test basic quantum-enhanced embedding first
    watermarked_img, quantum_signature = embedder.embed_watermark(
        test_image, secret, bit_length, use_quantum=True
    )
    
    print(f"Embedded secret: {secret}")
    print(f"Bit length: {bit_length}")
    print(f"Quantum signature: {quantum_signature[:32]}...")
    
    # Test basic quantum-enhanced extraction
    extracted_secret, is_verified = extractor.extract_watermark(
        watermarked_img, bit_length, quantum_signature
    )
    
    print(f"Extracted secret: {extracted_secret}")
    print(f"Verification status: {is_verified}")
    
    assert extracted_secret == secret, f"Expected {secret}, got {extracted_secret}"
    assert is_verified, "Quantum verification should pass"
    
    print("✅ Full quantum watermarking test passed!\n")

def main():
    """Run all quantum computing tests."""
    print("🚀 Starting Quantum Watermarking Tests...\n")
    
    try:
        test_quantum_key_generation()
        test_quantum_secret_sharing()
        test_quantum_watermark_encoder()
        test_quantum_entangled_shares()
        test_full_quantum_watermarking()
        
        print("🎉 All quantum computing tests passed successfully!")
        print("The system is ready for quantum-enhanced watermarking operations.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
