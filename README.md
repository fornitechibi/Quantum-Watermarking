# 🔬 Quantum Watermarking Images using Qiskit

[AI enabled Documentation](https://deepwiki.com/fornitechibi/Quantum-Watermarking)

A cutting-edge digital watermarking system that leverages **IBM Qiskit quantum computing** to enhance security in image watermarking. This project combines LSB (Least Significant Bit) steganography with quantum-enhanced Shamir's Secret Sharing scheme, utilizing real quantum circuits for cryptographic operations and random number generation.

## 🌟 Revolutionary Features

### Quantum Computing Integration

- **Qiskit Quantum Circuits**: Uses IBM's Qiskit framework for quantum computations
- **Quantum Random Number Generation**: True randomness from quantum superposition states
- **Quantum-Enhanced Secret Sharing**: Leverages quantum circuits for coefficient generation
- **Quantum Entangled Shares**: Creates quantum entangled states for additional security layers
- **Quantum Key Generation**: Generates cryptographically secure keys using quantum mechanics

### Advanced Watermarking Capabilities

- **LSB Watermarking**: Embeds integer watermarks into image pixels using least significant bit manipulation
- **Quantum-Enhanced Embedding**: Uses quantum bit encoding for enhanced security
- **Threshold Security**: Configurable quantum-enhanced threshold scheme (k-of-n)
- **Quantum Signature Verification**: Cryptographic signatures using quantum-generated salts
- **QR Code Generation**: Automatically generates QR codes for each secret share

### User Experience

- **Modern Web Interface**: Beautiful, responsive Flask-based web application
- **Real-time Quantum Operations**: Live quantum key generation via API
- **Metadata Management**: Download quantum metadata for enhanced verification
- **Image Processing**: Support for various image formats with automatic grayscale conversion
- **Secure Downloads**: Encrypted file download system for watermarked images

## 🔧 Quantum Technology Stack

- **Quantum Computing**: IBM Qiskit 1.2.4, Qiskit Aer 0.15.1, Qiskit Algorithms 0.3.1
- **Backend**: Python 3.13, Flask
- **Image Processing**: PIL (Pillow), OpenCV, NumPy
- **Cryptography**: Quantum-enhanced Shamir's Secret Sharing using SymPy
- **QR Codes**: qrcode library for share distribution
- **Frontend**: Modern HTML5, JavaScript, CSS with quantum-themed UI

## 📋 Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## 🚀 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Watermarking-Quantum
   ```

2. **Create and activate virtual environment**:

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` doesn't exist, install manually:

   ```bash
   pip install flask pillow opencv-python numpy qrcode sympy
   ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. **Access the web interface**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## � How Quantum Computing Enhances Security

### Quantum Watermark Embedding Process

1. **Quantum Key Generation**: Uses quantum superposition to generate truly random cryptographic keys
2. **Quantum-Enhanced Secret Sharing**:
   - Generates polynomial coefficients using quantum random number generation
   - Creates quantum entangled shares for additional security layers
   - Applies quantum polynomial evaluation with enhanced randomness
3. **Quantum Bit Encoding**: Encodes watermark bits using quantum superposition states
4. **LSB Embedding**: Embeds quantum-encoded watermark into image pixels
5. **Quantum Signature**: Creates cryptographic signatures using quantum-generated salts
6. **QR Generation**: Each share is encoded into QR codes with quantum metadata

### Quantum Watermark Extraction Process

1. **Share Collection**: Scan QR codes or input share values manually
2. **Quantum-Enhanced Reconstruction**: Uses quantum Lagrange interpolation
3. **LSB Extraction**: Extracts quantum-encoded watermark from image pixels
4. **Quantum Verification**: Verifies integrity using quantum signatures
5. **Key Recovery**: Applies quantum key operations to recover original watermark

### Quantum Security Advantages

- **True Randomness**: Quantum mechanics provides genuinely random numbers, not pseudo-random
- **Quantum Entanglement**: Creates unbreakable correlations between shares
- **Enhanced Cryptography**: Quantum-generated keys offer superior security
- **Tamper Detection**: Quantum signatures detect any unauthorized modifications
- **Future-Proof**: Resistant to classical and quantum computing attacks

## 🎯 Usage

### Embedding a Watermark

1. Navigate to the web interface
2. Upload your image (grayscale recommended for best results)
3. Enter an integer watermark value
4. Set threshold (minimum shares needed for reconstruction)
5. Set total number of shares to generate
6. Click "Embed & Generate Shares"
7. Download the watermarked image and save the generated QR codes

### Extracting a Watermark

1. Upload the watermarked image
2. Enter the bit length of the original watermark
3. Scan QR codes or manually enter share coordinates (x,y values)
4. Provide at least the threshold number of shares
5. Click "Extract Watermark" to recover the hidden data

## 📂 Project Structure

```
Watermarking-Quantum/
├── app.py                    # Main Flask application
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── watermark_lib/           # Core watermarking library
│   ├── __init__.py          # Package initialization
│   ├── embedder.py          # LSB watermark embedding
│   ├── extractor.py         # LSB watermark extraction
│   ├── secret_sharing.py    # Shamir's Secret Sharing implementation
│   └── qr_utils.py          # QR code generation utilities
├── templates/               # HTML templates
│   └── index.html           # Main web interface
├── static/                  # Static assets
│   ├── raw_img.jpg         # Sample image
│   └── qr_codes/           # Generated QR codes
├── downloads/              # Watermarked images storage
└── myenv/                  # Virtual environment
```

## 🔒 Security Features

- **Threshold Cryptography**: Requires multiple shares for secret reconstruction
- **Distributed Storage**: Shares can be stored separately for enhanced security
- **LSB Steganography**: Watermark is virtually invisible to the naked eye
- **QR Code Distribution**: Secure and convenient share distribution method
- **Integrity Verification**: Cross-validation between reconstruction and extraction

## 🎨 Technical Implementation

### LSB Watermarking Algorithm

- Converts watermark integer to binary representation
- Modifies the least significant bit of each pixel
- Preserves image quality while embedding data

### Secret Sharing Scheme

- Implements Shamir's (k,n) threshold scheme
- Uses polynomial interpolation for secret reconstruction
- Provides information-theoretic security

### QR Code Integration

- Encodes share coordinates as "x{i}={x_val},y{i}={y_val}"
- Generates high-contrast QR codes for reliable scanning
- Supports both manual entry and QR scanning workflows

## 🔬 Quantum API Endpoints

The application provides several quantum computing APIs for advanced users:

### Generate Quantum Key

```bash
GET /api/generate_quantum_key?bits=32
```

Returns a quantum-generated random key using Qiskit quantum circuits.

**Response:**

```json
{
  "quantum_key": 1234567890,
  "bit_length": 32,
  "hex_representation": "0x499602d2"
}
```

### Generate Quantum Entangled Shares

```bash
GET /api/quantum_shares/12345
```

Creates quantum entangled shares for a given secret using quantum circuits.

**Response:**

```json
{
  "secret": 12345,
  "quantum_shares": ["10110010", "01001101", "11010110"],
  "num_qubits": 8
}
```

## ⚛️ Quantum Computing Components

### QuantumKeyGenerator

- Generates truly random bits using quantum superposition
- Creates cryptographically secure keys for watermarking
- Uses Hadamard gates to put qubits in superposition states

### QuantumSecretSharing

- Enhances Shamir's Secret Sharing with quantum randomness
- Uses quantum circuits for polynomial coefficient generation
- Implements quantum-enhanced Lagrange interpolation

### QuantumWatermarkEncoder

- Creates quantum signatures for watermark integrity
- Encodes watermark bits using quantum superposition
- Provides tamper-evident quantum verification

### Quantum Entangled Shares

- Creates quantum entangled states between shares
- Uses quantum rotation gates for share differentiation
- Provides quantum correlation for enhanced security
