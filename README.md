# Quantum Watermarking Images using Qubit Shares

[AI enabled Documentation](https://deepwiki.com/fornitechibi/Quantum-Watermarking)

A sophisticated digital watermarking system that combines LSB (Least Significant Bit) steganography with Shamir's Secret Sharing scheme to create a secure and distributed watermark protection mechanism. This project provides both embedding and extraction capabilities through a user-friendly web interface.

## 🌟 Features

- **LSB Watermarking**: Embeds integer watermarks into image pixels using least significant bit manipulation
- **Secret Sharing**: Implements Shamir's Secret Sharing to distribute watermark data across multiple QR codes
- **Threshold Security**: Configurable threshold scheme (k-of-n) where only k shares are needed to reconstruct the secret
- **QR Code Generation**: Automatically generates QR codes for each secret share for easy distribution
- **Web Interface**: Flask-based web application for easy watermark embedding and extraction
- **Image Processing**: Support for various image formats with automatic grayscale conversion
- **Download Management**: Secure file download system for watermarked images

## 🔧 Technology Stack

- **Backend**: Python 3.13, Flask
- **Image Processing**: PIL (Pillow), OpenCV, NumPy
- **Cryptography**: Shamir's Secret Sharing implementation using SymPy
- **QR Codes**: qrcode library for share distribution
- **Frontend**: HTML5, JavaScript, CSS

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

## 💡 How It Works

### Watermark Embedding Process

1. **Input Processing**: Upload an image and specify an integer watermark
2. **Secret Sharing**: The watermark is split into multiple shares using Shamir's Secret Sharing
3. **LSB Embedding**: The original watermark is embedded into the image using LSB steganography
4. **QR Generation**: Each share is encoded into a QR code for secure distribution
5. **Output**: Watermarked image and QR codes containing the shares

### Watermark Extraction Process

1. **Share Collection**: Scan QR codes or manually input share values
2. **Secret Reconstruction**: Combine threshold number of shares to reconstruct the original watermark
3. **LSB Extraction**: Extract the watermark from the LSB of image pixels
4. **Verification**: Compare reconstructed and extracted values for integrity verification

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
