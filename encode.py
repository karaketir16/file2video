from itertools import islice
import os
import sys
import base64
import math
import json
import qrcode
import numpy as np
from multiprocessing import Pool, cpu_count
import av
from PIL import Image
from tqdm import tqdm
from reedsolo import RSCodec
from v2.v2 import encode_to_image

from createQR import create_qr
from checksum import checksum

from common import *


rs = None
grid_size = None

def read_in_chunks(file_object, chunk_size=1024):
    """Generator to read a file piece by piece."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def process_chunk(data):
    """Encode data chunk into BitCode and return as image."""
    data_encoded = rs.encode(data)
    length = len(data_encoded)

    length_encoded = rs.encode(length.to_bytes(4,'big'))

    data = length_encoded + data_encoded

    return encode_to_image(data, grid_size, 1080)

def encode_and_write_frames(frames, stream, container):
    """Encode frames and write to video container."""
    for frame in frames:
        video_frame = av.VideoFrame.from_ndarray(frame, format='rgb24')
        for packet in stream.encode(video_frame):
            container.mux(packet)

def create_video(src, dest, reedEC, grid, read_file_lazy = False):
    """Create video from source file using PyAV."""

    global rs, grid_size
    
    grid_size = grid
    rs = RSCodec(reedEC)

    reedK = GreedN - reedEC

    chunk_size = (reedK * ((grid_size*grid_size) // (GreedN * 8))) - (4 + reedEC)

    md5_checksum = checksum(src)
    file_stats = os.stat(src)
    file_size = file_stats.st_size
    chunk_count = math.ceil(file_size / chunk_size)
    print("chunk count:", chunk_count)

    pbar = tqdm(total=chunk_count, desc="Generating Frames")

    meta_data = {
        "Filename": os.path.basename(src),
        "ChunkCount": chunk_count,
        "Filehash": md5_checksum,
        "ConverterUrl": "https://github.com/karaketir16/file2video/tree/v2",
        "ConverterVersion": "python_v2",
        "FileSize:": file_size
    }

    first_frame_data = json.dumps(meta_data, indent=4)
    first_frame = create_qr(first_frame_data, width, height)

    # Open output file
    container = av.open(dest, mode='w')
    stream = container.add_stream('h264', rate=frame_rate)
    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'
    stream.options = {'crf': '40'}

    # Write the first frame
    video_frame = av.VideoFrame.from_ndarray(first_frame, format='rgb24')
    for packet in stream.encode(video_frame):
        container.mux(packet)

    # Process chunks in batches using multiprocessing
    with open(src, 'rb') as f, Pool(cpu_count()) as pool:
        entire_file = []
        if not read_file_lazy:
            entire_file = f.read()
        i = 0
        while True:

            chunks = []

            if read_file_lazy:
                chunks = list(islice(read_in_chunks(f, chunk_size), cpu_count()))
            else:
                for _ in range(cpu_count()):
                    chunks.append(entire_file[i: i + chunk_size])
                    if not chunks[-1]: #empty
                        chunks.pop()
                        break
                    i = i + chunk_size
            if not chunks:
                break

            frames = pool.map(process_chunk, chunks)
            encode_and_write_frames(frames, stream, container)
            pbar.update(len(frames))

    pbar.close()

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
    create_video(src, dest, GreedEC, Ggrid_size)
