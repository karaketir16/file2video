## File2Video

Convert any file to video. This allows you to upload it to YouTube and use YouTube as unlimited storage. The output video file size is typically about 3.2 times the size of the input file. If you upload video to youtube, please wait for HD processing of youtube.

### Example Usage
First, install the requirements:
```
pip install -r requirements.txt
```
We need OpenGL, GLib, and FFmpeg. Install them on Ubuntu/Debian with:
```
sudo apt-get install libgl1 libglib2.0-0 ffmpeg
```

Then, you can run the following command to convert a file to video:
```
python file2video.py --encode test/test100k.txt out.mp4
```
And you can run the following command to convert the video back to a file:
```
python file2video.py --decode out.mp4 ./
```
Or use a YouTube URL to retrieve the file:
```
python file2video --youtube-decode "https://youtu.be/LZ6mYm-2QNY" ./
```

### Example output
16 MB file [https://youtu.be/LZ6mYm-2QNY](https://youtu.be/LZ6mYm-2QNY)

100 MB file [https://youtu.be/ZfiJB3lqWlU](https://youtu.be/ZfiJB3lqWlU)


