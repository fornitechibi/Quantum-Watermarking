from flask import Flask, render_template, request, send_file, jsonify
from watermark_lib import embedder, extractor, secret_sharing, qr_utils
from watermark_lib.quantum_crypto import QuantumKeyGenerator, create_quantum_entangled_shares
from PIL import Image
import os
import io
import base64
import uuid
import json

app = Flask(__name__)
QR_FOLDER = 'static/qr_codes'
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(QR_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def image_to_base64(img):
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    watermarked_image_b64 = None
    qr_files = []
    extracted_watermark = ''
    watermarked_image_id = None
    watermark_bit_length = ''  # For pre-filling in form

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'embed':
            image_file = request.files.get('image')
            secret_text = request.form.get('watermark', '')
            try:
                secret_int = int(secret_text)
                threshold = int(request.form.get('threshold', 2))
                num_shares = int(request.form.get('num_shares', 3))
            except Exception:
                message = 'Please enter a valid integer watermark and numbers for threshold and shares.'
                return render_template('index.html', message=message)

            if image_file:
                image = Image.open(image_file)
                bit_len = secret_int.bit_length()
                watermark_bit_length = str(bit_len)

                # Embed watermark with quantum enhancement
                use_quantum = request.form.get('use_quantum', 'on') == 'on'
                
                if use_quantum:
                    watermarked_img, quantum_signature, quantum_key = embedder.embed_quantum_enhanced_watermark(
                        image.convert('L'), secret_int, bit_len
                    )
                    
                    # For quantum enhancement, create shares from the SAME secret that's embedded
                    # This ensures consistency between shares and watermark
                    enhanced_secret = (secret_int ^ quantum_key) % (2 ** bit_len)
                    shares = secret_sharing.split_secret(enhanced_secret, threshold, num_shares, use_quantum=use_quantum)
                else:
                    # For classical approach, use original secret for both shares and embedding
                    shares = secret_sharing.split_secret(secret_int, threshold, num_shares, use_quantum=use_quantum)

                # Generate QR codes for shares
                qr_files = []
                for (x, y) in shares:
                    data_str = f"x{x}={int(x)},y{x}={int(y)}"
                    filename = os.path.join(QR_FOLDER, f"share_{x}.png")
                    qr_utils.generate_qr(data_str, filename)
                    qr_files.append(f"/{filename}")

                if use_quantum:
                    # Store quantum metadata
                    metadata = {
                        'quantum_signature': quantum_signature,
                        'quantum_key': quantum_key,
                        'use_quantum': True,
                        'bit_length': bit_len,
                        'original_secret': secret_int,  # Store original for reference
                        'enhanced_secret': enhanced_secret  # Store enhanced for debugging
                    }
                    
                    # Create quantum entangled shares for additional security
                    # Use the actual bit length, but limit to reasonable quantum circuit size
                    num_qubits = min(bit_len, 16)  # Increased from 8 to 16 for larger secrets
                    quantum_shares = create_quantum_entangled_shares(secret_int, num_qubits)
                    metadata['quantum_shares'] = quantum_shares
                    
                else:
                    watermarked_img, quantum_signature = embedder.embed_watermark(
                        image.convert('L'), secret_int, bit_len, use_quantum=False
                    )
                    metadata = {
                        'use_quantum': False,
                        'bit_length': bit_len,
                        'original_secret': secret_int
                    }

                unique_id = str(uuid.uuid4())
                path = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}.png')
                watermarked_img.save(path)
                
                # Save metadata
                metadata_path = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}_metadata.json')
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f)
                
                watermarked_image_id = unique_id
                watermarked_image_b64 = image_to_base64(watermarked_img)
                
                quantum_status = "quantum-enhanced" if use_quantum else "classical"
                message = f'Watermark embedded ({quantum_status}) & shares generated! Bit length: {bit_len}'

        elif action == 'extract':
            try:
                bit_len = int(request.form.get('bit_len', 0))
                watermarked_file = request.files.get('watermarked_image')

                # Collect variable shares dynamically
                shares = []
                for key in request.form.keys():
                    if key.startswith('x'):
                        index = key[1:]
                        x_val_str = request.form.get(f'x{index}')
                        y_val_str = request.form.get(f'y{index}')
                        if x_val_str and y_val_str:
                            x = int(x_val_str)
                            y = int(y_val_str)
                            shares.append((x, y))

                if len(shares) < 2:
                    message = 'At least two shares are required to reconstruct the secret.'
                    return render_template('index.html', message=message)

                if watermarked_file and bit_len > 0:
                    # Check if quantum enhancement was used
                    use_quantum_extract = request.form.get('use_quantum_extract', 'on') == 'on'
                    
                    # Robust reconstruction with error handling
                    try:
                        secret_quantum = secret_sharing.reconstruct_secret(shares, use_quantum=True)
                        secret_classical = secret_sharing.reconstruct_secret(shares, use_quantum=False)
                        
                        # Choose the best reconstruction result
                        if secret_quantum < 0 and secret_classical > 0:
                            secret_int = secret_classical
                            reconstruction_method = "classical (quantum gave negative result)"
                        elif secret_classical < 0 and secret_quantum > 0:
                            secret_int = secret_quantum
                            reconstruction_method = "quantum (classical gave negative result)"
                        elif abs(secret_quantum) == abs(secret_classical):
                            secret_int = abs(secret_quantum)  # Use absolute value
                            reconstruction_method = "corrected absolute value"
                        else:
                            # Use the method requested by user
                            secret_int = secret_quantum if use_quantum_extract else secret_classical
                            reconstruction_method = "quantum" if use_quantum_extract else "classical"
                            
                        print(f"Debug: Quantum reconstruction: {secret_quantum}")
                        print(f"Debug: Classical reconstruction: {secret_classical}")
                        print(f"Debug: Using {reconstruction_method}: {secret_int}")
                        
                    except Exception as e:
                        print(f"Debug: Reconstruction error: {e}")
                        # Fallback to classical reconstruction
                        secret_int = secret_sharing.reconstruct_secret(shares, use_quantum=False)
                        reconstruction_method = "fallback classical"

                    watermarked_img = Image.open(watermarked_file)
                    
                    # Try to load metadata if available
                    metadata_file = request.files.get('metadata_file')
                    quantum_signature = None
                    quantum_key = None
                    
                    if metadata_file:
                        try:
                            metadata = json.load(metadata_file)
                            quantum_signature = metadata.get('quantum_signature')
                            quantum_key = metadata.get('quantum_key')
                        except:
                            pass
                    
                    # Extract watermark
                    if quantum_signature and quantum_key:
                        # For quantum-enhanced extraction, we need to be careful about what we compare
                        extracted_int, is_verified = extractor.extract_quantum_enhanced_watermark(
                            watermarked_img.convert('L'), bit_len, quantum_signature, quantum_key
                        )
                        verification_status = "✓ Verified" if is_verified else "✗ Not Verified"
                        
                        # The correct comparison: shares give enhanced_secret, extraction gives original_secret
                        # So we need to convert the share reconstruction back to original
                        if quantum_key:
                            original_from_shares = (secret_int ^ quantum_key) % (2 ** bit_len)
                        else:
                            original_from_shares = secret_int
                            
                        if original_from_shares != extracted_int:
                            message = f"Warning: Share reconstruction → original ({original_from_shares}) and direct extraction ({extracted_int}) differ. Enhanced secret from shares: {secret_int}. Method: {reconstruction_method}. {verification_status}"
                        else:
                            message = f'Watermark extracted successfully using {reconstruction_method}! Original secret: {extracted_int}. {verification_status}'
                            
                    else:
                        # Classical extraction
                        extracted_int, is_verified = extractor.extract_watermark(
                            watermarked_img.convert('L'), bit_len, quantum_signature
                        )
                        verification_status = "✓ Verified" if is_verified else "✗ Not Verified" if quantum_signature else "No verification"
                        
                        if secret_int != extracted_int:
                            message = f"Warning: Share reconstruction ({secret_int}) and watermark extraction ({extracted_int}) differ. Method: {reconstruction_method}. {verification_status}"
                        else:
                            message = f'Watermark extracted successfully using {reconstruction_method}! {verification_status}'

                    extracted_watermark = str(extracted_int)
                else:
                    message = 'Watermarked image and bit length must be provided.'
            except Exception as e:
                message = 'Extraction failed: ' + str(e)

    return render_template('index.html', message=message,
                           qr_files=qr_files,
                           watermarked_image=watermarked_image_b64,
                           extracted_watermark=extracted_watermark,
                           watermarked_image_id=watermarked_image_id,
                           watermark_bit_length=watermark_bit_length)

@app.route('/download/<image_id>')
def download_image(image_id):
    path = os.path.join(DOWNLOAD_FOLDER, f'{image_id}.png')
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path, mimetype='image/png', as_attachment=True, download_name='watermarked_image.png')

@app.route('/download/<image_id>/metadata')
def download_metadata(image_id):
    path = os.path.join(DOWNLOAD_FOLDER, f'{image_id}_metadata.json')
    if not os.path.exists(path):
        return "Metadata not found", 404
    return send_file(path, mimetype='application/json', as_attachment=True, download_name='quantum_metadata.json')

@app.route('/api/generate_quantum_key')
def generate_quantum_key():
    """Generate a quantum random key via API."""
    try:
        bit_length = int(request.args.get('bits', 32))
        if bit_length > 1024:  # Safety limit
            return jsonify({'error': 'Bit length too large'}), 400
        
        qrng = QuantumKeyGenerator()
        quantum_key = qrng.generate_quantum_key(bit_length)
        
        return jsonify({
            'quantum_key': quantum_key,
            'bit_length': bit_length,
            'hex_representation': hex(quantum_key)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quantum_shares/<int:secret>')
def get_quantum_shares(secret):
    """Generate quantum entangled shares for a secret."""
    try:
        # Use appropriate number of qubits for the secret size
        num_qubits = min(max(secret.bit_length(), 4), 16)  # Min 4, max 16 qubits
        quantum_shares = create_quantum_entangled_shares(secret, num_qubits)
        
        return jsonify({
            'secret': secret,
            'quantum_shares': quantum_shares,
            'num_qubits': num_qubits,
            'secret_bit_length': secret.bit_length()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
