
from PIL import Image
import numpy as np
import qrcode


def create_qr(data_str, width, height, box_size=10, error_correction_level=qrcode.constants.ERROR_CORRECT_L):
    """Generate a QR code as a NumPy array from data string with specified box size and error correction level."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction_level,
        box_size=box_size,
        border=4,
    )
    qr.add_data(data_str)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    pil_img = img.resize((width, height), Image.Resampling.NEAREST)  # Use NEAREST for less interpolation blur
    return np.array(pil_img)
