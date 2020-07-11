import cv2
from lsh_util import img_list_loader

img_list= img_list_loader("C:\\Users\\LSH\\Downloads\\Test\\107_1_cam01_swoon01_place06_night_spring_swoon_140_50_4213",extension='jpg')
img_label= img_list_loader("C:\\Users\\LSH\\Downloads\\Test\\Test",extension='txt')

width ,height = 960, 540
for i in range(len(img_list)):
    img= img_list[i]
    if i<300: 
        continue
    else:
        label= img_label[i-300]
        with open(label, 'r') as f:
            label= f.readlines()
    
    for l in label:
        print(i)
        l=l.split(" ")
        c_x= width*float(l[1])
        c_y= height*float(l[2])
        w= width*float(l[3])
        h= height*float(l[4])

        x1,y1,x2,y2= int(c_x - (w/2)),int(c_y - (h/2)),int(c_x + (w/2)),int(c_y + (h/2))

        # print(type(l[1]))
        # img= cv2.rectangle(img, (100,100), (500,500), (255,255,0), 4)
        
            # print(l)
        
        img= cv2.imread(img)
        img= cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 2)
        cv2.imshow("a",img)
        cv2.waitKey(50)