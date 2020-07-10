import os
from xml.etree.ElementTree import parse
import datetime
import argparse
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
    min=time.split(":")[-2]
    sec=time.split(":")[-1]
    
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
def extract_stf(xml_path):
    xml_path="D:\\ai-hub\\실신\\outsidedoor_01\\100-6\\100-6_cam01_swoon01_place02_day_spring.xml"
    tree = parse(xml_path)
    root = tree.getroot()
    obj = root.findall('object')
    action = [x.findtext("action") for x in obj]
    frame=[]
    for a in root.iter('action'):
        name= a.findtext("actionname")
        if name == "falldown":
            start_frame= [x.findtext("start") for x in a.findall('frame')]

    return start_frame

def video2frame(invideofilename, save_path,frame):
    vidcap = cv2.VideoCapture(invideofilename)
    count = 0
    img_cnt =0
    target_frame =int(frame)
    fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    
    #해당 action이 발생하기전 얼마만큼의 시간을 볼건지에 대한 변수
    pre_trim_sec= 10
    if target_frame < fps * pre_trim_sec:
            target_frame = fps * pre_trim_sec

    vidcap.set(1,target_frame- fps * pre_trim_sec)

    fps_trans_rate= round(fps/15)

    while True:
        success,image = vidcap.read()
        if not success:
            break
        if count % fps_trans_rate ==0:
            image=cv2.resize(image,dsize=(1920,1080),interpolation=cv2.INTER_AREA)
            fname = 'img_{}.jpg'.format("{0:05d}".format(img_cnt))
            cv2.imwrite(os.path.join(save_path, fname), image) # save frame as JPEG file
            cv2.imshow("a",image)
            cv2.waitKey(10)
            img_cnt+=1
            if img_cnt % 100 ==0:
                print(img_cnt)
            if img_cnt >300:
                break
        count += 1
    print("{} images are extracted in {}.". format(count, save_path))

def extract_video(src_folder, dst_folder):
    for outdoor in img_list_loader(src_folder,is_dir=True):
        for fold_num in img_list_loader(outdoor,is_dir=True):            
            for vid_name in img_list_loader(fold_num,extension='mp4'):
                xml_path=vid_name.split(".")[0]+".xml"
                label=parsing_label(xml_path)
                dir_name= naming(vid_name.split("\\")[-1],label)
                stf= extract_stf(xml_path)
                for f in stf:
                    path= os.path.join(dst_folder,dir_name+"+"+f)
                    print(path)
                    mkdir(path)
                    video2frame(vid_name,path,f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str, help="src folder")
    parser.add_argument('dst', type=str, help="src folder")

    args =parser.parse_args()
    # extract_video("D:\\ai-hub\\싸움\\","D:\\ai2020_prprc\\rgb_vid\\fight")
    extract_video(args.src, args.dst)