import cv2
from lsh_util import img_list_loader
import argparse

# img_list= img_list_loader("C:\\Users\\LSH\\Downloads\\Test\\107_1_cam01_swoon01_place06_night_spring_swoon_140_50_4213",extension='jpg')
# img_label= img_list_loader("C:\\Users\\LSH\\Downloads\\Test\\Test",extension='txt')

def xywh2xyxy(c_x,c_y,w,h):
    x1,y1,x2,y2= c_x - (w/2),c_y - (h/2),c_x + (w/2),c_y + (h/2)
    return x1,y1,x2,y2

if __name__ == "__main__":
    width ,height = 960, 540
    parser = argparse.ArgumentParser()
    parser.add_argument('img_list', type=str, help="img folder")
    parser.add_argument('img_label', type=str, help="label folder")
    args =parser.parse_args()

    img_list= img_list_loader(args.img_list,extension='jpg')
    img_label= img_list_loader(args.img_label,extension='txt')


    for i in range(len(img_list)):
        img= img_list[i]
        if i<300: 
            label= ["0 0 0 0 0"]

        else:
            label= img_label[i-300]
            with open(label, 'r') as f:
                label= f.readlines()
            if len(label) ==0:
                label= ["0 0 0 0 0"]
        for l in label:
            l=l.split(" ")
            c_x,c_y,w,h= float(l[1]), float(l[2]), float(l[3]), float(l[4])
            x1,y1,x2,y2= xywh2xyxy(c_x,c_y,w,h)
            x1,x2 = round(width*x1), round(width*x2)
            y1,y2= round(height*y1), round(height*y2)
            
            img= cv2.imread(img)
            img= cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 2)
            cv2.imshow("a",img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                exit()