import os
import cv2
from xml.etree.ElementTree import parse
from datetime import timedelta

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

class Preprc_situation_video():
    def __init__(self,path):
        self.data_dir_path= path

        xml_list = img_list_loader(self.data_dir_path, 'xml')
        tree= parse(xml_list[1])
        root = tree.getroot()
        #lv 1
        event= root.findall("event")
        objects= root.findall("object")

        #lv2,3 
        #event series
        self.e_name = [e.findtext("eventname") for e in event]
        self.start_time= [e.findtext("starttime") for e in event]
        self.start_time = int(self.start_time[0].split(":")[1])*60 + int(self.start_time[0].split(":")[2].split(".")[0])
        self.duration= [e.findtext("duration") for e in event]

        #object seriese
        self.o_name = [o.findtext("objectname") for o in objects]
        
        position= objects[0].findall('position')
        self.p_keyframe= [p.findtext("keyframe") for p in position]
        
        p_keypoint= position[0].findall("keypoint")        
        self.pk_x = [int(o.findtext("x")) for o in p_keypoint]
        self.pk_y = [int(o.findtext("y")) for o in p_keypoint]
        
        action= objects[0].findall('action')
        self.a_name= [a.findtext('actionname') for a in action]


    def monitoring_data(self, path):   
        cap= cv2.VideoCapture(path)
        i=0
        
        time_length= self.start_time
        fps=round(cap.get(cv2.CAP_PROP_FPS))
        frame_no = time_length*fps -1000
        
        cap.set(1, int(self.p_keyframe[0]))
        ret, frame = cap.read()
        ptr=(self.pk_x[0],self.pk_y[0])
        l1 = (self.pk_x[0],self.pk_y[0]-100)
        l2 = (self.pk_x[0],self.pk_y[0]-200)
        l3 = (self.pk_x[0],self.pk_y[0]-300)

        frame= cv2.putText(frame,'action name:'+self.a_name[0],l1,cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5)
        frame= cv2.putText(frame,'keyframe:'+str(self.p_keyframe[0]),l2,cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5)
        frame= cv2.putText(frame,'object_name: '+self.o_name[0],l3,cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),5)            
        frame= cv2.line(frame,ptr,ptr, (0,0,255),50)
        frame=cv2.resize(frame, (1000,500))
        cv2.imshow('video',frame)
        cv2.waitKey(0)

        cap.set(1, frame_no)
        ret, frame = cap.read()
        frame=cv2.resize(frame, (1000,500))
        cv2.imshow('video',frame)

        while(cap.isOpened()):
            frame_id= round(cap.get(1))
            print(frame_id)
            ret, frame = cap.read()
            frame=cv2.resize(frame, (1000,500))

            if ret:    
                cv2.imshow('video',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()