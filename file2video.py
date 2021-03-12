# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import qrcode
import numpy as np
import cv2
import base64
import sys


#https://stackoverflow.com/a/519653/8328237
def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


width = 1080
height = 1080
dim = (width, height)
chunk_size = 500
frame_rate = 20.0


def create_qr(data_str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=4,
    )
    qr.add_data(data_str)
    # qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    # print(type(img))
    cv_img = np.array(img)
    return cv_img[:, :, ::-1].copy()
    # Convert RGB to BGR

def create_video():
    counter = 0

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(sys.argv[2], fourcc, frame_rate, dim)

    with open(sys.argv[1], 'rb') as f:
        for piece in read_in_chunks(f, chunk_size):
            frame = create_qr(base64.b64encode(piece).decode('ascii'))
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            out.write(frame)
            print(counter)
            counter += 1


    # Release everything if job is finished
    out.release()








# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python file2video.py source_file output_file.mp4")
        assert False
    create_video()


#https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5

#https://github.com/cisco/openh264/releases
