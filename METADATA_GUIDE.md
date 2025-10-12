# 🔐 Quantum Metadata in Watermarking System

## What is Quantum Metadata?

When you embed a watermark using **quantum enhancement**, the system generates additional cryptographic data that ensures maximum security and verification. This metadata is stored in a JSON file alongside your watermarked image.

## 📋 Contents of Quantum Metadata

The metadata file contains several critical pieces of information:

### 1. **Quantum Signature** 🔑

```json
{
  "quantum_signature": "1943219125dfa2e30199dcc0eee8b4ea5f8a7b9c3d4e..."
}
```

- **Purpose**: Cryptographic signature created using quantum-generated salt
- **Security**: Uses true quantum randomness for tamper detection
- **Function**: Verifies that the watermark hasn't been modified

### 2. **Quantum Key** 🗝️

```json
{
  "quantum_key": 962718395
}
```

- **Purpose**: Additional encryption key generated using quantum circuits
- **Security**: XORed with the original watermark for enhanced protection
- **Function**: Required to decrypt the watermark back to its original value

### 3. **System Information** ℹ️

```json
{
  "use_quantum": true,
  "bit_length": 11,
  "quantum_shares": ["10101010101", "01010101010", "10101010101"]
}
```

- **use_quantum**: Indicates quantum enhancement was used
- **bit_length**: Number of bits in the original watermark
- **quantum_shares**: Quantum entangled backup shares

## 🔄 Watermark Extraction Process

### Without Metadata (Basic Extraction)

```
Input: Watermarked Image + Shares + Bit Length
↓
1. Reconstruct secret from shares (classical/quantum)
2. Extract watermark from image LSB
3. Compare results
4. Basic verification only
```

### With Metadata (Enhanced Extraction)

```
Input: Watermarked Image + Shares + Bit Length + Metadata
↓
1. Load quantum signature and key from metadata
2. Reconstruct secret from shares
3. Extract quantum-enhanced watermark from image
4. Decrypt using quantum key (XOR reversal)
5. Verify using quantum signature
6. Full cryptographic verification ✅
```

## 🛡️ Security Benefits of Using Metadata

| Feature              | Without Metadata    | With Metadata           |
| -------------------- | ------------------- | ----------------------- |
| **Tamper Detection** | ❌ Basic            | ✅ Cryptographic        |
| **Key Security**     | ❌ Share-based only | ✅ Quantum key + shares |
| **Verification**     | ❌ Comparison only  | ✅ Digital signature    |
| **Future-Proof**     | ❌ Classical crypto | ✅ Quantum-resistant    |

## 📱 How to Use in the Web Interface

### During Embedding:

1. Upload your image
2. Enter watermark (e.g., `2004`)
3. ✅ Keep "Enable Quantum Enhancement" checked
4. Click "Embed Watermark & Generate Shares"
5. **Download both**:
   - 📥 Watermarked image
   - 🔐 Quantum metadata file

### During Extraction:

1. Enter share values from QR codes
2. Set correct bit length
3. Upload the watermarked image
4. ✅ Keep "Use Quantum-Enhanced Extraction" checked
5. **Upload quantum metadata file** ← This is the key step!
6. Click "Extract & Verify Watermark"

## 🔬 Technical Details

### Quantum Signature Creation:

```python
def create_quantum_signature(self, watermark_data: str) -> str:
    # Generate quantum random salt using QRNG
    salt_bits = self.qrng.generate_quantum_random_bits(64)
    salt = int(salt_bits, 2).to_bytes(8, 'big')

    # Create hash with quantum-generated salt
    hasher = hashlib.sha256()
    hasher.update(watermark_data.encode())
    hasher.update(salt)  # Quantum salt provides true randomness

    return hasher.hexdigest() + salt.hex()
```

### Quantum Key Usage:

```python
# During embedding:
enhanced_secret = original_secret ^ quantum_key

# During extraction:
original_secret = enhanced_secret ^ quantum_key
```

## ⚠️ Important Notes

### **Always Keep Metadata Safe!**

- The metadata file is **required** for full quantum verification
- Without it, you lose the quantum security benefits
- Store it separately from the watermarked image for security

### **File Naming Convention:**

- Watermarked image: `{uuid}.png`
- Metadata file: `{uuid}_metadata.json`
- Both use the same UUID for linking

### **Compatibility:**

- **With metadata**: Full quantum security + verification
- **Without metadata**: Falls back to classical reconstruction
- **Mixed mode**: Will show warnings but still extracts

## 🚨 Error Messages Explained

### `"Warning: Share reconstruction (-116) and watermark extraction (167) differ"`

- **Cause**: Reconstruction algorithm gave negative result
- **Solution**: The system now auto-corrects using multiple methods
- **New behavior**: Shows which reconstruction method was used

### `"Metadata not found"`

- **Cause**: Metadata file wasn't uploaded or is corrupted
- **Solution**: Upload the correct `{uuid}_metadata.json` file
- **Fallback**: System will work without metadata but with reduced security

## 🎯 Best Practices

1. **Always download both files** when embedding
2. **Upload metadata file** when extracting for full security
3. **Use quantum enhancement** for sensitive watermarks
4. **Store metadata separately** from the watermarked image
5. **Keep backups** of both watermark shares AND metadata

## 🔮 Future Enhancements

When full quantum computers become available:

- Metadata will include **quantum circuit state snapshots**
- **Quantum key distribution** protocols for secure metadata sharing
- **Quantum error correction** codes in the metadata
- **Post-quantum cryptographic** signatures
