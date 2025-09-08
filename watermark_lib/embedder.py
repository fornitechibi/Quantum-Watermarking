from PIL import Image
import numpy as np

def int_to_bits(i: int, length: int) -> str:
    bits = bin(i)[2:]
    return bits.zfill(length)

def embed_watermark(image: Image.Image, secret_int: int, bit_length: int) -> Image.Image:
    bits = int_to_bits(secret_int, bit_length)
    img_array = np.array(image.convert('L'), dtype=np.uint8)
    flat_img = img_array.flatten()
    bits = bits[:len(flat_img)]  # safety truncate
    for i, bit in enumerate(bits):
        pixel = flat_img[i]
        pixel = (pixel & 0xFE) | int(bit)
        flat_img[i] = pixel
    watermarked_array = flat_img.reshape(img_array.shape)
    return Image.fromarray(watermarked_array)
