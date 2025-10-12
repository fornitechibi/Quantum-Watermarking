from PIL import Image
import numpy as np
from .quantum_crypto import QuantumWatermarkEncoder

def extract_watermark(image: Image.Image, bit_length: int, quantum_signature: str = None) -> tuple:
    """
    Extract watermark using classical or quantum-enhanced LSB extraction.
    
    Args:
        image: PIL Image object to extract watermark from
        bit_length: Expected length of the watermark in bits
        quantum_signature: Optional quantum signature for verification
        
    Returns:
        Tuple of (extracted_secret, is_verified)
    """
    img_array = np.array(image.convert('L'))
    flat_img = img_array.flatten()
    bits = ''.join(str(flat_img[i] & 1) for i in range(bit_length))
    extracted_secret = int(bits, 2)
    
    is_verified = True
    if quantum_signature:
        # Verify quantum signature
        quantum_encoder = QuantumWatermarkEncoder()
        watermark_data = f"{extracted_secret}:{bit_length}"
        is_verified = quantum_encoder.verify_quantum_signature(watermark_data, quantum_signature)
    
    return extracted_secret, is_verified


def extract_quantum_enhanced_watermark(image: Image.Image, bit_length: int, 
                                     quantum_signature: str, quantum_key: int) -> tuple:
    """
    Extract watermark with full quantum enhancement.
    
    Args:
        image: PIL Image object to extract watermark from
        bit_length: Expected length of the watermark in bits
        quantum_signature: Quantum signature for verification
        quantum_key: Quantum key used during embedding
        
    Returns:
        Tuple of (original_secret, is_verified)
    """
    # Extract the enhanced secret first (this is what was actually embedded)
    enhanced_secret, _ = extract_watermark(image, bit_length)
    
    # Verify signature against the enhanced secret (what was signed during embedding)
    if quantum_signature:
        watermark_data = f"{enhanced_secret}:{bit_length}"
        quantum_encoder = QuantumWatermarkEncoder()
        is_verified = quantum_encoder.verify_quantum_signature(watermark_data, quantum_signature)
    else:
        is_verified = False
    
    # Reverse the XOR operation with quantum key to get original secret
    original_secret = (enhanced_secret ^ quantum_key) % (2 ** bit_length)
    
    return original_secret, is_verified


def verify_watermark_integrity(extracted_secret: int, bit_length: int, 
                             quantum_signature: str) -> bool:
    """
    Verify the integrity of an extracted watermark using quantum signature.
    
    Args:
        extracted_secret: The extracted secret integer
        bit_length: Length of the secret in bits
        quantum_signature: Quantum signature to verify against
        
    Returns:
        True if watermark is verified, False otherwise
    """
    quantum_encoder = QuantumWatermarkEncoder()
    watermark_data = f"{extracted_secret}:{bit_length}"
    return quantum_encoder.verify_quantum_signature(watermark_data, quantum_signature)
