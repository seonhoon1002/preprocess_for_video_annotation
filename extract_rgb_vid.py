import os
from xml.etree.ElementTree import parse
import datetime
import cv2
def img_list_loader(path, extension = 'pickle',is_dir=False):
    """
    :param path: 이미지를 불러올 디렉토리 명입니다.
    :param extension: 선택할 확장자 입니다.
    :return: 파일 경로가 있는 imgs_list를 불러옵니다.
    """
    imgs_list = os.listdir(path)
    imgs_list = sorted(imgs_list)
    if is_dir:
        result = [os.path.join(path, name) for name in imgs_list]
    else:
        result = [os.path.join(path, name) for name in imgs_list if name.split(".")[1] == extension]
    return result
def m2s(time):
    min=time.split(":")[1]
    sec=time.split(":")[2]
    
    total_sec=float(min) * 60 + float(sec)
    
    return str(int(total_sec))

def naming(vid_name, label):
    event, start_time,duration =label[0][0],label[1][0],label[2][0]
    start_time= m2s(start_time)
    duration =m2s(duration)

    vid_name= vid_name.split(".")[0] +"+"+event+ "+"+start_time+"+"+duration
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

def video2frame(invideofilename, save_path):
    vidcap = cv2.VideoCapture(invideofilename)
    count = 0
    img_cnt =0
    while True:
        success,image = vidcap.read()
        if not success:
            break
        if count %3 ==0:
            image=cv2.resize(image,dsize=(256,256),interpolation=cv2.INTER_AREA)
            fname = 'img_{}.jpg'.format("{0:05d}".format(img_cnt))
            cv2.imwrite(os.path.join(save_path, fname), image) # save frame as JPEG file
            img_cnt+=1
            if img_cnt % 100 ==0:
        count += 1
    print("{} images are extracted in {}.". format(count, save_path))

def extract_video(src_folder, dst_folder):
    for outdoor in img_list_loader(src_folder,is_dir=True):
        for fold_num in img_list_loader(outdoor,is_dir=True):            
            for vid_name in img_list_loader(fold_num,extension='mp4'):
                xml_path=vid_name.split(".")[0]+".xml"
                label=parsing_label(xml_path)
                dir_name= naming(vid_name.split("\\")[-1],label)
                path= os.path.join(dst_folder,dir_name)
                
                mkdir(path)
                video2frame(vid_name,path)


extract_video("D:\\ai-hub\\폭행\\","D:\\ai2020_prprc\\rgb_vid")