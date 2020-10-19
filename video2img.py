import os
from xml.etree.ElementTree import parse
import datetime
import argparse
import cv2
from lsh_util import get_filepaths_in_dir, get_dirpaths_in_dir
import datetime



def m2s(time):
    min=time.split(":")[-2]
    sec=time.split(":")[-1]
    
    total_sec=float(min) * 60 + float(sec)
    
    return str(int(total_sec))

def naming(vid_name, label):
    event, start_time,duration =label[0][0],label[1][0],label[2][0]
    start_time= m2s(start_time)
    duration =m2s(duration)

    vid_name= vid_name.split(".")[0] +"_"+event+ "_"+start_time+"_"+duration
    return vid_name

def parsing_label(xml_path):
    tree = parse(xml_path)
    root = tree.getroot()
    event = root.findall('event')

    event_name = [x.findtext("eventname") for x in event]
    start_time = [x.findtext("starttime") for x in event]
    duration = [x.findtext("duration") for x in event]

    return event_name, start_time, duration

def mkdir(path):
    try:
        if not(os.path.isdir(path)):
            os.makedirs(os.path.join(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
def extract_start_points(xml_path):
    tree = parse(xml_path)
    root = tree.getroot()
    obj = root.findall('object')
    frame=[]
    start_points=[]
    h=root.iter('header')
    
    header= [x.findtext("fps") for x in h]
    fps= int(header[0])

    for e in root.iter('event'):
        start_points=[e.findtext('starttime')]
        duration= [e.findtext('duration')]
        start_time=strtime2fps(e.findtext('starttime'),fps)
        duration= strtime2fps(e.findtext('duration'),fps)
        if event_type=='abdonment':
            start_points=[start_time+ duration]
        else:
            start_points=[start_time]
        # if name != None:
        #     start_points= [x.findtext("start") for x in e.findall('frame')]

    return start_points
def strtime2fps(str_time,fps):
    str_time= str_time.split('.')[0].split(":")
    sec=int(str_time[-1])
    mm= int(str_time[-2])
    str_time=(mm * 60 + sec)*fps

    return str_time
def video2imgs(invideofilename, save_path,frame,wh_size,fps,pre_trim_sec=15,duration=20):
    vidcap = cv2.VideoCapture(invideofilename)
    count = 0
    img_cnt =0
    target_frame =int(frame)
    video_fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    
    if target_frame < fps * pre_trim_sec:
            target_frame = fps * pre_trim_sec

    vidcap.set(1,target_frame- (fps * pre_trim_sec))

    fps_trans_rate= round(video_fps/fps)

    while True:
        success,image = vidcap.read()
        # print(image.shape)
        if not success:
            break
        if count % fps_trans_rate ==0:
            image=cv2.resize(image,dsize=wh_size,interpolation=cv2.INTER_AREA)
            fname = 'img_{}.jpg'.format("{0:05d}".format(img_cnt))
            cv2.imwrite(os.path.join(save_path, fname), image) # save frame as JPEG file
            cv2.imshow("a",cv2.resize(image,dsize=wh_size,interpolation=cv2.INTER_AREA))
            cv2.waitKey(10)
            img_cnt+=1
            if img_cnt % 100 ==0:
                print(img_cnt)
            if img_cnt >(duration * fps):
                break
        count += 1
    print("{} images are extracted in {}.". format(count, save_path))

def cvt_video2img_AIHUB(src_folder, dst_folder,fps=5,wh_size=(720,500), exclusion_range=580, pre_trim_sec=10,duration=30):
    """
    exclusion_range: This arg define exclusion area to prevents the overlapping of same event situation. 
    pre_trim_sec: This arg define how long set the time before event happen
    wh_size: width, height of converted image
    fps: frame per second of converted image

    """
    for outdoor in get_dirpaths_in_dir(path=src_folder):
        for fold_num in get_dirpaths_in_dir(path=outdoor):
            for vid_name in get_filepaths_in_dir(path=fold_num,extension='mp4')[:1]:
                
                xml_path=vid_name.split(".")[0]+".xml"
                label=parsing_label(xml_path)

                #dir_name for saving converted imgs
                dir_name= naming(vid_name.split("\\")[-1],label)
                dir_name=dir_name.replace('-','_')
                #extract start_points because there could be several event points in the one video
                start_points= extract_start_points(xml_path)
                #prev start point 
                prev_sp=0
                for f in start_points:
                    f=int(f)
                    
                    if f < (prev_sp-exclusion_range):
                        continue
                        
                    print(f)
                    save_path= os.path.join(dst_folder,dir_name+"_"+str(f))
                    mkdir(save_path)
                    video2imgs(vid_name,save_path,f,wh_size,fps,pre_trim_sec,duration)
                    prev_sp = f 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, help="src folder")
    parser.add_argument('--dst', type=str, help="dst folder")
    parser.add_argument('--fps', type=int, help="fps")
    parser.add_argument('--wh_size', type=int,nargs="+" ,help="width height")
    parser.add_argument('--duration', type=int ,help="duration second")
    parser.add_argument('--event',default='fight', type=str ,help="event type")

    args =parser.parse_args()
    global event_type
    event_type=args.event
    cvt_video2img_AIHUB(args.src, args.dst,args.fps,tuple(args.wh_size),duration=args.duration)