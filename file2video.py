import os
import sys
import base64
import math
import hashlib
import json
import qrcode
import numpy as np
from multiprocessing import Pool, cpu_count
import av
from PIL import Image

# Constants
chunk_size = 500
frame_rate = 20.0
width = 1080
height = 1080

def read_in_chunks(file_object, chunk_size=1024):
    """Generator to read a file piece by piece."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def checksum(large_file):
    """Calculate MD5 checksum for file."""
    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    with open(large_file, 'rb') as a_file:
        chunk = a_file.read(block_size)
        while chunk:
            md5_object.update(chunk)
            chunk = a_file.read(block_size)
    return md5_object.hexdigest()

def create_qr(data_str, box_size=10, error_correction_level=qrcode.constants.ERROR_CORRECT_L):
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
    cv_img = np.array(pil_img)
    return cv_img[:, :, ::-1].copy()  # Convert RGB to BGR


def create_frame(chunk, frame_id):
    """Create and save a video frame from a data chunk."""
    frame = create_qr(base64.b64encode(chunk).decode('ascii'))
    return frame

def encode_frames(chunks):
    """Encode chunks into frames and write to video using multiprocessing."""
    with Pool(cpu_count()) as pool:
        frame_ids = range(len(chunks))
        frames = pool.starmap(create_frame, zip(chunks, frame_ids))
    
    print("done encoding, creating video...")
    return frames

def create_video(src, dest):
    """Create video from source file using PyAV."""
    md5_checksum = checksum(src)
    file_stats = os.stat(src)
    file_size = file_stats.st_size
    chunk_count = math.ceil(file_size / chunk_size)

    meta_data = {
        "Filename": os.path.basename(src),
        "ChunkCount": chunk_count,
        "Filehash": md5_checksum,
        "ConverterUrl": "https://github.com/karaketir16/file2video",
        "ConverterVersion": "python_v1"
    }

    first_frame_data = json.dumps(meta_data, indent=4)
    first_frame = create_qr(first_frame_data)

    # Open output file
    container = av.open(dest, mode='w')
    stream = container.add_stream('h264', rate=frame_rate)
    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'

    stream.options = {'crf': '40'}  # Lower values mean better quality


    # Write the first frame
    video_frame = av.VideoFrame.from_ndarray(first_frame, format='bgr24')
    for packet in stream.encode(video_frame):
        container.mux(packet)

    # Process each chunk in the file
    chunks = []
    with open(src, 'rb') as f:
        for piece in read_in_chunks(f, chunk_size):
            chunks.append(piece)

    frames = encode_frames(chunks)

    for frame in frames:
        video_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
        for packet in stream.encode(video_frame):
            container.mux(packet)

    # Finalize the video file
    for packet in stream.encode():
        container.mux(packet)

    container.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python file2video.py source_file output_file.mp4")
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    create_video(src, dest)
