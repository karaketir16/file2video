import cv2
import json
import os
import sys
import base64
import logging
from pyzbar import pyzbar
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from checksum import checksum

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def apply_preprocessing(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return threshold

def read_barcode(preprocessed_frame):
    barcodes = pyzbar.decode(preprocessed_frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        return True, barcode_info
    return False, None

def process_frame(frame):
    preprocessed_frame = apply_preprocessing(frame)
    success, data = read_barcode(preprocessed_frame)
    if not success:
        logging.warning("Failed to read QR code")
        return None  # Return None if no barcode is found
    return data

def read_video(cap, dest_folder):

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=total_frames, desc="Processing Frames")

    ret, first_frame = cap.read()
    if not ret:
        logging.error("Cannot read first frame")
        return

    metadata = process_frame(first_frame)
    if metadata is None:
        logging.error("No QR code in first frame; cannot proceed")
        return
    meta_data = json.loads(metadata)
    dest = os.path.join(dest_folder, meta_data["Filename"])
    file = open(dest, "wb")

    # Start worker processes
    num_workers = cpu_count()

    with Pool(num_workers) as pool:
        while cap.isOpened():
            frames = []
            done = False
            for _ in range(num_workers):
                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
                else:
                    done = True
                    break

            datas = pool.map(process_frame, frames)

            pbar.update(len(frames))

            for data in datas:
                file.write(base64.b64decode(data))

            if done:
                break


    file.close()
    cap.release()
    pbar.close()

    logging.info("Verify file integrity")
    md5_sum = checksum(dest)
    assert md5_sum == meta_data["Filehash"], "Data corrupted"
    logging.info("File integrity verified: ")
    logging.info(dest)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error("Usage: python script.py source_file.mp4 destination_folder")
        sys.exit(1)
    src = sys.argv[1]
    dest_folder = sys.argv[2]

    cap = cv2.VideoCapture(src)

    read_video(cap, dest_folder)
