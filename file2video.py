from encode import create_video
from decode_video import decode
from youtube_decode import youtube_decode
import argparse
import sys
import os


def is_valid_path_docker(destination_folder):
    # Get absolute path of the destination folder
    abs_dest_folder = os.path.abspath(destination_folder)
    # Get absolute path of the current directory
    current_directory = os.path.abspath('.')
    # Ensure the destination folder is a subdirectory of the current directory
    return os.path.commonpath([abs_dest_folder]) == os.path.commonpath([abs_dest_folder, current_directory])


def enc_file(source_file, output_video):
    print (f"Encoding {source_file} to {output_video}")
    create_video(source_file, output_video)

def dec_video(source_video, destination_folder, docker_mode):
    if docker_mode:
        if not is_valid_path_docker(destination_folder):
            print("Destination folder should be subfolder of the current directory")
            return
    print (f"Decoding {source_video} to {destination_folder}")
    decode(source_video, destination_folder)

def y_decode(video_url, destination_folder, docker_mode):
    if docker_mode:
        if not is_valid_path_docker(destination_folder):
            print("Destination folder should be subfolder of the current directory")
            return
    print (f"Decoding {video_url} to {destination_folder}")
    youtube_decode(video_url, destination_folder)


def main():

    # First, check if '--docker' is in the command line arguments
    docker_mode = '--docker' in sys.argv
    if docker_mode:
        sys.argv.remove('--docker')  # Remove it so it doesn't interfere with the main parser

    docker_usage = """\
docker run --rm -v $(pwd):/data karaketir16/file2video [-h]  [--encode source_file output_video] 
                                                        [--decode source_video destination_folder] 
                                                        [--youtube-decode youtube_url destination_folder]"""
    
    if docker_mode:
        parser = argparse.ArgumentParser(description="Program to encode files into videos and decode videos back to files.", usage=docker_usage)
    else:
        parser = argparse.ArgumentParser(description="Program to encode files into videos and decode videos back to files.")

    # Optional argument for encoding
    parser.add_argument("--encode", nargs=2, metavar=('source_file', 'output_video'), 
                        help="Encode a file into a video: source_file output_video.mp4")
    
    # Optional argument for decoding
    parser.add_argument("--decode", nargs=2, metavar=('source_video', 'destination_folder'), 
                        help="Decode a video to a file: source_video.mp4 destination_folder")
    
    # Optional argument for YouTube video decoding
    parser.add_argument("--youtube-decode", nargs=2, metavar=('youtube_url', 'destination_folder'), 
                        help="Decode a video from a YouTube URL to a file: 'youtube_url' destination_folder")

    
    args = parser.parse_args()

    # Check which command is used and call the corresponding function
    if args.encode:
        enc_file(*args.encode)
    elif args.decode:
        dec_video(*args.decode, docker_mode)
    elif args.youtube_decode:
        y_decode(*args.youtube_decode, docker_mode)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()