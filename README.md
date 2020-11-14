# preprocess_for_video_annotation
This repository is made for video annotation preprocess that is uploaded in AI_HUB in Korea.
My code transform video to images, which can modify fps, extracting event duration and size

## code install

<pre>
<code>
pip install -r requirements.txt
</code>
</pre>

## code implementation

If you want to convert video in AI_HUB, enter the bellow command.

<pre>
<code>
python video2img --src [video dir path] --dst [img dir path] --fps [fps] --wh_size [width height] --duration [duration sec]
</code>
</pre>

Like this

<pre>
<code>
python video2img.py --src D:\ai-hub\abdonment --dst D:\ai-hub_prprc\abdonment --fps 10 --wh_size 1280 720 --duration 30
</code>
</pre>

## File structure
It is necessary to set video folder like bellow image
<pre>
<code>
src_video_folder
 |
 |
 |_________1.mp4
 |_________2.mp4
 ....
 |_________100.mp4
</code>
</pre>

My model automatically sets the structure like bellow image.

Just know my model how form the structure.
<pre>
<code>
dst_video_folder
 |
 |
 |_________1 img foldoer
 |              |_________img_00000.jpg    
 |              |_________img_00001.jpg
 |              |_________img_00002.jpg
 |              ...
 |_________2 img foldoer
 |              |_________img_00000.jpg    
 |              |_________img_00001.jpg
 |              |_________img_00002.jpg
 |              ...
 |_________100 img foldoer
</code>
</pre>