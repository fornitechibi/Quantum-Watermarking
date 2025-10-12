from PIL import Image
import numpy as np
from .quantum_crypto import QuantumWatermarkEncoder, QuantumKeyGenerator

def int_to_bits(i: int, length: int) -> str:
    bits = bin(i)[2:]
    return bits.zfill(length)

def embed_watermark(image: Image.Image, secret_int: int, bit_length: int, use_quantum: bool = True) -> tuple:
    """
    Embed watermark using classical or quantum-enhanced LSB steganography.
    
    Args:
        image: PIL Image object to embed watermark into
        secret_int: Secret integer to embed
        bit_length: Length of the secret in bits
        use_quantum: Whether to use quantum-enhanced embedding
        
    Returns:
        Tuple of (watermarked_image, quantum_signature)
    """
    bits = int_to_bits(secret_int, bit_length)
    
    if use_quantum:
        # For now, we'll just use regular bits but add quantum signature
        # The quantum enhancement is in the signature and key generation
        encoded_bits = bits
        
        # Create quantum signature for integrity verification
        watermark_data = f"{secret_int}:{bit_length}"
        quantum_encoder = QuantumWatermarkEncoder()
        quantum_signature = quantum_encoder.create_quantum_signature(watermark_data)
    else:
        encoded_bits = bits
        quantum_signature = None
    
    img_array = np.array(image.convert('L'), dtype=np.uint8)
    flat_img = img_array.flatten()
    
    # Embed the encoded bits
    embedded_bits = encoded_bits[:len(flat_img)]  # safety truncate
    for i, bit in enumerate(embedded_bits):
        pixel = flat_img[i]
        pixel = (pixel & 0xFE) | int(bit)
        flat_img[i] = pixel
    
    watermarked_array = flat_img.reshape(img_array.shape)
    watermarked_image = Image.fromarray(watermarked_array)
    
    return watermarked_image, quantum_signature


def embed_quantum_enhanced_watermark(image: Image.Image, secret_int: int, bit_length: int) -> tuple:
    """
    Embed watermark with full quantum enhancement including quantum keys.
    
    Args:
        image: PIL Image object to embed watermark into
        secret_int: Secret integer to embed
        bit_length: Length of the secret in bits
        
    Returns:
        Tuple of (watermarked_image, quantum_signature, quantum_key)
    """
    # Generate quantum key for additional security
    qrng = QuantumKeyGenerator()
    quantum_key = qrng.generate_quantum_key(16)  # Use smaller key to avoid overflow
    
    # XOR secret with quantum key for enhanced security (ensure result fits in bit_length)
    enhanced_secret = (secret_int ^ quantum_key) % (2 ** bit_length)
    
    # Create quantum signature for the enhanced secret that gets embedded
    watermark_data = f"{enhanced_secret}:{bit_length}"
    quantum_encoder = QuantumWatermarkEncoder()
    quantum_signature = quantum_encoder.create_quantum_signature(watermark_data)
    
    # Embed the enhanced secret without creating another signature
    bits = int_to_bits(enhanced_secret, bit_length)
    img_array = np.array(image.convert('L'), dtype=np.uint8)
    flat_img = img_array.flatten()
    
    # Embed the bits
    embedded_bits = bits[:len(flat_img)]  # safety truncate
    for i, bit in enumerate(embedded_bits):
        pixel = flat_img[i]
        pixel = (pixel & 0xFE) | int(bit)
        flat_img[i] = pixel
    
    watermarked_array = flat_img.reshape(img_array.shape)
    watermarked_image = Image.fromarray(watermarked_array)
    
    return watermarked_image, quantum_signature, quantum_key
