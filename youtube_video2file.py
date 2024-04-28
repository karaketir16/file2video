import cv2
import sys
import yt_dlp
import os

from video2file import read_video

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python video2file.py \"https://video_url\" destination_folder")
        sys.exit(1)

    src = sys.argv[1]
    dest_folder = sys.argv[2]
    output_file = f"{dest_folder}/downloaded_video.mp4"

    # Create a yt-dlp configuration to download the video
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_file,
        'noplaylist': True,
        'quiet': True,
        'merge_output_format': 'mp4',  # Ensure the output is mp4 if separate streams are downloaded
    }

    # Use yt-dlp to download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([src])

    # Check if the file is downloaded and exists
    if os.path.exists(output_file):
        # Open the downloaded video file using OpenCV
        cap = cv2.VideoCapture(output_file)

        # Read and process the video
        read_video(cap, dest_folder)
    else:
        print("Failed to download video.")
        sys.exit(1)
