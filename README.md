## File2Video

Convert any file to video that consist from QR codes. You can upload it to youtube, and use youtube as unlimited storage. Output video size likely 150 times larger than input file. (If you will upload the video to youtube and download back, file size reduced. Youtube can compress video better)
So Youtube approximately compresses the file by 10 so at the start you create a file that is 150x the original file size but after downloading from youtube you dowload a filet that is 15x the size the original for the output barcode video, the converter for video 2 file converts succesfully the compressed youtube version. This has been tested. 01/09/2023

### Example Usage
First install requirements
```
pip install -r requirements.txt
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
If you receive an error like `Could not find encoder for codec id 27: Encoder not found` change the line from file2video.py
```
fourcc = cv2.VideoWriter_fourcc(*'X264')
```
with 
```
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
```

But this time output video size likely 450 times larger then input. 
