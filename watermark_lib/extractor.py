from PIL import Image
import numpy as np

def extract_watermark(image: Image.Image, bit_length: int) -> int:
    img_array = np.array(image.convert('L'))
    flat_img = img_array.flatten()
    bits = ''.join(str(flat_img[i] & 1) for i in range(bit_length))
    return int(bits, 2)
