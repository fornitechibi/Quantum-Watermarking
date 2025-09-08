from flask import Flask, render_template, request, send_file
from watermark_lib import embedder, extractor, secret_sharing, qr_utils
from PIL import Image
import os
import io
import base64
import uuid

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

                shares = secret_sharing.split_secret(secret_int, threshold, num_shares)

                qr_files = []
                for (x, y) in shares:
                    data_str = f"x{x}={int(x)},y{x}={int(y)}"
                    filename = os.path.join(QR_FOLDER, f"share_{x}.png")
                    qr_utils.generate_qr(data_str, filename)
                    qr_files.append(f"/{filename}")

                watermarked_img = embedder.embed_watermark(image.convert('L'), secret_int, bit_len)

                unique_id = str(uuid.uuid4())
                path = os.path.join(DOWNLOAD_FOLDER, f'{unique_id}.png')
                watermarked_img.save(path)
                watermarked_image_id = unique_id

                watermarked_image_b64 = image_to_base64(watermarked_img)
                message = f'Watermark embedded & shares generated! Bit length: {bit_len}'

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
                    secret_int = secret_sharing.reconstruct_secret(shares)

                    watermarked_img = Image.open(watermarked_file)
                    extracted_int = extractor.extract_watermark(watermarked_img.convert('L'), bit_len)

                    if secret_int != extracted_int:
                        message = f"Warning: Share reconstruction ({secret_int}) and watermark extraction ({extracted_int}) differ."

                    extracted_watermark = str(extracted_int)
                    message = 'Watermark extracted successfully!'
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
