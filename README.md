## File2Video

Convert any file to video that consist from QR codes. You can upload it to youtube, and use youtube as unlimited storage. Output video size likely 24 times larger than input file.

### Example Usage
First install requirements
```
pip install -r requirements.txt
```
We need opengl, glib, zbar, ffmpeg

install it ubuntu/debian
```
sudo apt-get install libgl1 libglib2.0-0 libzbar0 ffmpeg
```

Then you can run to convert file to video
```
python file2video.py test/test100k.txt out.mp4
```
And you can run to convert back to file
```
python video2file.py out.mp4 .
```
Or give it a youtube url
```
python youtube_video2file.py "https://youtu.be/z7Op3XNvWxw" .
```

### Example output
https://youtu.be/z7Op3XNvWxw

### Notes
It shows `WARNING: decoder/databar.c:1248: _zbar_decode_databar: Assertion "seg->finder >= 0" failed.`, but this warning does not create problem for decoding.