# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import base64
import sys
import hashlib
import json
from pyzbar import pyzbar
import os
from tqdm import tqdm

def apply_preprocessing(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply adaptive thresholding
    #threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return threshold

def read_the_barc(frame):
    preprocessed_frame = apply_preprocessing(frame)
    barcodes = pyzbar.decode(preprocessed_frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        return True, barcode_info

    return False, 0


def read_the_barc_wo_preprocess(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        return True, barcode_info

    return False, 0

# Existing functions remain unchanged...

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


# def read_the_barc(frame):
#     barcodes = pyzbar.decode(frame)
#     for barcode in barcodes:
#         barcode_info = barcode.data.decode('utf-8')
#         return True, barcode_info
#     return False, 0

def checker(frame):
    res_with, _ = read_the_barc(frame)
    res_wo, _ = read_the_barc_wo_preprocess(frame)

    if res_with == True and res_wo == True:
        pass
    elif res_with == True and res_wo == False:
        print("Better with Preprocessing")
    elif res_with == False and res_wo == True:
        print("Worse with Preprocessing")

def read_vid():
    cap = cv2.VideoCapture(src)
    ret, first_frame = cap.read()
    res, retval = read_the_barc(first_frame)
    if not res:
        print("Cannot read first frame QR")
        return
    meta_data = json.loads(retval)

    # type MetaData struct {
    # 	Filename         string
    # 	ChunkCount       int
    # 	Filehash         string
    # 	ConverterUrl     string
    # 	ConverterVersion string
    # }

    print(retval)
    dest = os.path.join(dest_folder, meta_data["Filename"])
    file = open(dest, "wb")

    pbar = tqdm(total=meta_data["ChunkCount"])
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:

            checker(frame)

            res, retval = read_the_barc(frame)
            assert res
            file.write(base64.b64decode(retval))
            pbar.update(1)
        else:
            break

    pbar.close()
    file.close()

    md5_sum = checksum(dest)
    if md5_sum != meta_data["Filehash"]:
        print("Data corrupted")
    else:
        print("Done!")



if __name__ == '__main__':
    global src
    global dest_folder
    if len(sys.argv) < 3:
        print("usage: python video2file.py source_file.mp4 destination_folder")
        assert False
    src = sys.argv[1]
    dest_folder = sys.argv[2]
    read_vid()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


#https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5

