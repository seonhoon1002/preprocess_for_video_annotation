import os,sys
import numpy as np
import cv2
from PIL import Image
from multiprocessing import Pool
import argparse
import skvideo.io
import scipy.misc
from lsh_util import img_list_loader
import imageio

def ToImg(raw_flow,bound):
    '''
    this function scale the input pixels to 0-255 with bi-bound

    :param raw_flow: input raw pixel value (not in 0-255)
    :param bound: upper and lower bound (-bound, bound)
    :return: pixel value scale from 0 to 255
    '''
    flow=raw_flow
    flow[flow>bound]=bound
    flow[flow<-bound]=-bound
    flow-=-bound
    flow*=(255/float(2*bound))
    return flow

def save_flows(flows,rgb_vid_path,save_dir,num,bound):
    '''
    To save the optical flow images and raw images
    :param flows: contains flow_x and flow_y
    :param image: raw image
    :param save_dir: save_dir name (always equal to the video id)
    :param num: the save id, which belongs one of the extracted frames
    :param bound: set the bi-bound to flow images
    :return: return 0
    '''
    #rescale to 0~255 with the bound setting

    flow_x=ToImg(flows[...,0],bound)
    flow_y=ToImg(flows[...,1],bound)

    folder_name= rgb_vid_path.split("\\")[-1]
    save_dir =os.path.join(save_dir,folder_name)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    #save the flows
    save_x=os.path.join(save_dir,'x_{:05d}.jpg'.format(num))
    save_y=os.path.join(save_dir,'y_{:05d}.jpg'.format(num))
    flow_x_img=Image.fromarray(flow_x)
    flow_y_img=Image.fromarray(flow_y)
    imageio.imwrite(save_x,flow_x_img)
    imageio.imwrite(save_y,flow_y_img)

def dense_flow(src,dst,step_size,bound):
    frame_list= img_list_loader(src,extension='jpg')
    flow_num=0
    for idx in range(len(frame_list))[:len(frame_list)-step_size-1]:
        frame=cv2.imread(frame_list[idx])
        prev_image=frame
        prev_gray=cv2.cvtColor(prev_image,cv2.COLOR_RGB2GRAY)
        for t in range(step_size):
            frame=cv2.imread(frame_list[idx+t+1])
            image=frame
            gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
            dtvl1 =cv2.optflow.DualTVL1OpticalFlow_create()
            flowDTVL1=dtvl1.calc(prev_gray,gray,None)
            save_flows(flowDTVL1,src,dst,flow_num,bound) #this is to save flows and img.
            flow_num+=1


def get_video_list():
    video_list=[]
    for cls_names in os.listdir(videos_root):
        cls_path=os.path.join(videos_root,cls_names)
        for video_ in os.listdir(cls_path):
            video_list.append(video_)
    video_list.sort()
    return video_list,len(video_list)

def extract_flow(src_folder,dst_folder,step_size=5,bound=15):
    for rgb_vid_folder in img_list_loader(src_folder,is_dir=True):
        dense_flow(rgb_vid_folder, dst_folder,step_size,bound)
if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src', type=str, help="src folder")
    parser.add_argument('dst', type=str, help="dst folder")

    parser.add_argument('--step_size',default=5, type=int, help="step size")
    args =parser.parse_args()
    extract_flow(args.src, args.dst,step_size=args.step_size)
    # extract_flow("D:\\ai2020_prprc\\rgb_vid\\dump","D:\\ai2020_prprc\\flow\\dump",step_size=args.step_size)