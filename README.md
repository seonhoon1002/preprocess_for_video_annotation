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


This is example

<pre>
<code>
python video2img.py --src D:\ai-hub\abdonment --dst D:\ai-hub_prprc\abdonment --fps 10 --wh_size 1280 720 --duration 30
</code>
</pre>

## File structure
<pre>
<code>
src
 |__

</code>
</pre>