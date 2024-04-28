# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import qrcode
import numpy as np
import cv2
import base64
import sys
import os
import math
from tqdm import tqdm
import hashlib
import json


meta_data = {}

width = 1080
height = 1080
dim = (width, height)
chunk_size = 500
frame_rate = 20.0


file_size = 0
chunk_count = 0

#https://stackoverflow.com/a/519653/8328237
def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def checksum(large_file):
    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    a_file = open(large_file, 'rb')
    chunk = a_file.read(block_size)
    while chunk:
        md5_object.update(chunk)
        chunk = a_file.read(block_size)
    md5_hash = md5_object.hexdigest()

    return md5_hash

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
    
    
    
def create_frame(chunk):
    frame = create_qr(base64.b64encode(chunk).decode('ascii'))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return frame
from multiprocessing import Pool

def create_video():
    global meta_data
    global file_size
    global chunk_count
    
    md5_checksum = checksum(src)
    file_stats = os.stat(src)
    file_size = file_stats.st_size
    chunk_count = math.ceil(file_size / chunk_size)

    meta_data["Filename"] = os.path.basename(src)
    meta_data["ChunkCount"] = chunk_count
    meta_data["Filehash"] = md5_checksum
    meta_data["ConverterUrl"] = "https://github.com/karaketir16/file2video"
    meta_data["ConverterVersion"] = "python_v1"

    first_frame = create_qr(json.dumps(meta_data, indent=4))
    first_frame = cv2.resize(first_frame, dim, interpolation=cv2.INTER_AREA)

    chunks = []
    with open(sys.argv[1], 'rb') as f:
        for piece in read_in_chunks(f, chunk_size):
            chunks.append(piece)

    # Create a multiprocessing Pool
    pool = Pool()  
    frames = pool.map(create_frame, chunks)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(dest, fourcc, frame_rate, dim)
    out.write(first_frame)
    for frame in frames:
        out.write(frame)

    # Release everything if job is finished
    out.release()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global src
    global dest
    if len(sys.argv) < 3:
        print("usage: python file2video.py source_file output_file.mp4")
        assert False
    src = sys.argv[1]
    dest = sys.argv[2]
    create_video()


#https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5

#https://github.com/cisco/openh264/releases
