import cv2
import json
import os
import sys
import logging
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from checksum import checksum
from reedsolo import RSCodec

from common import *

from v2.v2 import decode_from_image

rs = None
reedEC = None
grid_size = None

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_frame(frame):
    data = decode_from_image(frame, grid_size)

    length_encoded = data[ : (4 + reedEC)]
    length_decoded, _, _ = rs.decode(length_encoded)

    length = int.from_bytes(length_decoded, 'big')

    data_encoded = data[ (4 + reedEC) :  (4 + reedEC) + length]

    data, _, errata_pos = rs.decode(data_encoded)

#    if len(errata_pos) > 0:
#        print("Fixed Number of Errors in this frame: ", len(errata_pos))

    return data

def decode_video(cap, dest_folder, reedEC, grid_size):

    globals()['grid_size'] = grid_size
    globals()['rs'] = RSCodec(nsym = reedEC, nsize = global_reedN)
    globals()['reedEC'] = reedEC

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total= (total_frames - 1), desc="Processing Frames")

    ret, first_frame = cap.read()
    if not ret:
        logging.error("Cannot read first frame")
        return

    metadata = process_frame(first_frame)
    if metadata is None:
        logging.error("No QR code in first frame; cannot proceed")
        return
    meta_data = json.loads(metadata.decode('utf8'))
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
                file.write(data)

            if done:
                break

    file.close()
    cap.release()
    pbar.close()

    logging.info("Verifying file integrity for %s", dest)
    md5_sum = checksum(dest)
    if md5_sum != meta_data["Filehash"]:
        logging.error("Data corrupted for file %s", dest)
        raise ValueError("Data corrupted")
    logging.info("File integrity verified: %s", dest)

def decode(src, dest_folder, reedEC, grid_size):
    cap = cv2.VideoCapture(src)
    decode_video(cap, dest_folder, reedEC, grid_size)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error("Usage: python script.py source_file.mp4 destination_folder")
        sys.exit(1)
    src = sys.argv[1]
    dest_folder = sys.argv[2]

    decode(src, dest_folder, global_reedEC, global_gridSize)

