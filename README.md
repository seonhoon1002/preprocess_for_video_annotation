# preprocess_for_video_annotation
This repository is made for video annotation preprocess that is uploaded in AI_HUB in Korea.
My code transform video to images, which can modify fps, extracting event duration and size

## supporting os
This project can only run in window  
Someday, I will make model that can be run in Ubuntu

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
python video2img --src [video dir path] --dst [img dir path] --fps [fps] --wh_size [width height] --duration [duration sec] --extenstion [video extension]
</code>
</pre>

Like this

<pre>
<code>
python video2img.py --src D:\data\first_dataset_2020_10\raw_video\fire --dst D:\data\first_dataset_2020_10\refine_video\fire --fps 10 --wh_size 1280 720 --duration 30 --extension 'mp4'
</code>
</pre>

## File structure
It is necessary to set video folder like bellow image  
It doesn't have to set xml file(If you have no xml, my model automatically ignore xml file)
<pre>
<code>
src_video_folder
 |
 |_________outsidedoor01
 |              |_________1-5
 |              |          |____1.mp4    
 |              |          |____1.xml
 |              |          |____2.mp4
 |              |          |____2.xml
 |              |
 |              |_________1-6
 |              |          |____1.mp4    
 |              |          |____1.xml
 |              |          |____2.mp4
 |              |          |____2.xml
 |              |_________1-7
 |              
 ....
 |_________outsidedoor02
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