# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 14:16:27 2021
d
@author: Jinyong Kim
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 11:13:02 2020

@author: Donghee Lee
"""

"""detection by hsv circle"""
"""영상마다 이 코드의 hsv 범위 바꿔줘야된다!!"""
"""Label : circle x, y, r"""

import numpy as np
import cv2
from hsv_tracker2 import HSV_Tracker
from edge_tracker import EDGE_Tracker
import random
import csv
from augmentation_data import img_aug
import glob





# #원본 파일 해상도
# x_orig = 1280
# y_orig = 720

#각 영상 할때마다 input 주소 바꿔주고, 그에 맞는 purple 범위로 바꿔야 함 
video_number=1
file = 'C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d/datalabeling.csv'%video_number
dataset = np.loadtxt(file, delimiter=',', dtype=np.string_)
dataset=np.float32(dataset[:,0:4])

path = glob.glob("C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d/data/*.jpg"%video_number)



#for rooftop
# purple_lower = (110, 80, 20)
# purple_upper = (170, 255, 255)

#for outdoor
#purple_lower = (113, 75, 14)
#purple_upper = (173, 255, 255)

#for lab
# purple_lower = (118, 95, 25)
# purple_upper = (162, 255, 255)

#for hand work
purple_lower = (158, 46, 124)
purple_upper = (255, 163, 206)

# done = False

# first_frame = 1

track1 = EDGE_Tracker()




aug = img_aug(purple_lower, purple_upper)


crop_mode = 1 #crop_mode 1이면 크롭 있는 것, 0이면 크롭 없는 test


frame_skip = 3 # 다음 프레임까지 스킵 수(이건 안건드는게 좋을거에요)
skip_count = 0

num_of_crops = 3 # 프레임당 크롭 수
crop_count = 0

aug_num = 1 # 크롭 당 aug 개수(brightness, ch.shift)
aug_count = 0

aug_rot_num = 3 # 프레임 당 rotate 수
aug_rot_count = 0

curr_frame = 0 #영상에서 현재 프레임
frame_idx = 0 #저장할 크롭 이름, 기본은 0, 이어서 할거면 다음 이름 - 1

norm = 0

label_x = []
label_y = []

label_w = []
label_h = []
#label_r = []
label_file_name = []



# Read until video is completed
for i in range(len(path)):
    img=cv2.imread("C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d"%video_number+"/data/%d.jpg" %(i+1),cv2.IMREAD_COLOR)
    #원본 파일 해상도
    y_orig, x_orig = img.shape[:2]
     

    frameClone = img.copy()
    

    ######################################################################
    
    # rect = track2.hsv_track(frameClone)
    # x, y, w, h = rect
    # cv2.rectangle(frameClone, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # mid_x = (x + x + w) / 2
    # mid_y = (y + y + h) / 2
    
    
    x, y, w,h = dataset[i][0],dataset[i][1],dataset[i][2],dataset[i][3]
    

    mid_x = (x+x+w)/2
    mid_y = (y+y+h)/2
    w_w = w
    h_h = h
    
   
    
   
    
        
    #######################################################################    
    while crop_count < num_of_crops and crop_mode == 1 :
        
        
  
        mid_x = (x+x+w)/2
        mid_y = (y+y+h)/2
        w_w = w
        h_h = h 

    
        if w != 0 : 
            norm = 1
       
        
        
        
                
        
        # mid_x = x
        # mid_y = y
        
        
        
        
        small = int(min((5/8) * w_w, mid_x, x_orig - mid_x) - 2)
        large = int(min((5/4) * w_w, mid_x, x_orig - mid_x))
        
        small_y = int(min((5/8) * h_h, mid_y, y_orig - mid_y) - 2)
        large_y = int(min((5/4) * h_h, mid_y, y_orig - mid_y) + 2)
        # small = min(r / 2, r * 1.5)
        #large = max(x - r, y - r, x_orig - (x + r), y_orig - (y + r))
      
        
       
        #rand_size = np.random.randint(int(w_w/2)+int(small/2), int(w_w/2) + int(small))
        rand_size = np.random.randint(small, large)
        rand_size_y = np.random.randint(small_y, large_y)
    
    
        small_shift_x = -min(rand_size - w_w/2,mid_x - rand_size )-4
        large_shift_x = min(rand_size - w_w/2, x_orig - mid_x -rand_size)+4
        
        small_shift_y = -min(rand_size_y - h_h/2,mid_y - rand_size_y )-1
        large_shift_y = min(rand_size_y - h_h/2, y_orig - mid_y -rand_size_y)+1
   
    
        rand_shift_x=np.random.randint(small_shift_x, large_shift_x)
        rand_shift_y=np.random.randint(small_shift_y, large_shift_y)
   
        
       
        crop = frameClone[round(mid_y) - round(rand_size) + rand_shift_y : round(mid_y) + round(rand_size) + rand_shift_y, round(mid_x) - round(rand_size) + rand_shift_x : round(mid_x) + round(rand_size) + rand_shift_x]
        
        mid_y = mid_y - (round(mid_y) - round(rand_size) + rand_shift_y)
        mid_x = mid_x - (round(mid_x) - round(rand_size) + rand_shift_x)
        
        # if mid_x - w_w/2 < 0 or mid_y - h_h/2 or mid_x + w_w/2 > frameClone.shape[1] or mid_y + h_h/2 > frameClone.shape[0]:
        #     continue
        if crop.shape[1] * crop.shape[0] ==0:
            continue
        trans = 400 / crop.shape[1]
        trans2 = 400 / crop.shape[0]
        crop = cv2.resize(crop, dsize=(400, 400), interpolation=cv2.INTER_AREA)
        
        mid_x = mid_x * trans
        mid_y = mid_y * trans2
        w_w = w_w * trans
        h_h = h_h * trans2
        
        # if not ( 0< w_w < 400 and 0 < h_h < 400):
        #     continue


        
        crop2=crop.copy()
        cropclone=crop.copy()
        crop2 = cv2.rectangle(crop2, (int(mid_x - w_w/2),int(mid_y - h_h/2)),(int(mid_x + w_w/2),int(mid_y + h_h/2)) , (145,128,186),-1)
        
        
       
        
      
        #frame 저장
        if crop.shape[0] == crop.shape[1] and norm == 1 :
            
            trans = 400 / crop.shape[1]
            
            frame_idx = frame_idx + 1
            norm = 0
            
            crop = cv2.resize(crop, dsize=(400, 400), interpolation=cv2.INTER_AREA)
            
            mid_x = mid_x * trans
            mid_y = mid_y * trans
            # w = w * trans
            # h = h * trans
            w_w = w_w * trans
            h_h = h_h * trans
            
            
            cv2.imwrite('C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, crop)
            label_x = np.append(label_x, mid_x - w_w/2)
            label_y = np.append(label_y, mid_y - h_h/2)
          
            label_w= np.append(label_w, w_w)
            label_h = np.append(label_h, h_h)
            
            label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
            
            
            while aug_count < aug_num :
                aug1 = aug.brightness(crop)
                frame_idx = frame_idx + 1
                cv2.imwrite('C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, aug1)
                label_x = np.append(label_x, mid_x - w_w/2)
                label_y = np.append(label_y, mid_y - h_h/2)
              
                label_w= np.append(label_w, w_w)
                label_h = np.append(label_h, h_h)
                
                label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
                
                
                aug2 = aug.ch_shift(crop)
                frame_idx = frame_idx + 1
                cv2.imwrite('C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, aug2)
                label_x = np.append(label_x, mid_x - w_w/2)
                label_y = np.append(label_y, mid_y - h_h/2)
              
                label_w= np.append(label_w, w_w)
                label_h = np.append(label_h, h_h)
                label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
                
                aug_count = aug_count + 1
                
            aug_count = 0
            
            
            while aug_rot_count < aug_rot_num : 
                
                # aug3, mid_y_r, mid_x_r, w_r, h_r = aug.rotation(frame)
                #frameClone: 원본 frameClone2: circle 그린 사본 -> hsv_tracker2를 활용할 수 있음.
                aug3, x_r, y_r, w_w,h_h = aug.rotation_rect(cropclone,crop2)
                # aug3, mid_y_r, mid_x_r, r_r = aug.rotation_circ(frame)
                
                trans_r = 400 / aug3.shape[0]
                
                if aug3.shape[0] == aug3.shape[1]:
                    
                    frame_idx = frame_idx + 1
                    
                    aug3 = cv2.resize(aug3, dsize=(400, 400), interpolation=cv2.INTER_AREA)
                    x_r = x_r * trans_r
                    y_r = y_r * trans_r
                    w_w = w_w * trans_r
                    h_h = h_h * trans_r
                    
                
                    cv2.imwrite('C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, aug3)
                
                #x, y, diameter 저장
                    label_x = np.append(label_x, x_r)
                    label_y = np.append(label_y, y_r)
                  
                    label_w= np.append(label_w, w_w)
                    label_h = np.append(label_h, h_h)
                    label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
                    
                    aug_rot_count = aug_rot_count + 1
                
                        
            aug_rot_count = 0    
      
        crop_count = crop_count + 1
       
    if crop_count == num_of_crops:
        crop_count = 0
        skip_count = 0
        norm = 0
   

# data = [label_x, label_y, label_w, label_h, label_file_name]
data = [label_x, label_y, label_w,label_h, label_file_name]
data = np.transpose(data)
with open('C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d'%video_number+'/cropdata.csv', 'w', newline = '') as f:
    wt = csv.writer(f)
    wt.writerows(data)


# contour checking
file = 'C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d/cropdata.csv'%(video_number)
data = np.loadtxt(file, delimiter=',', dtype=np.string_)
data=np.float32(data[:,0:4])
path = glob.glob("C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d"%(video_number)+"/cropdata/*.jpg")

for i in range(len(path)):
    img=cv2.imread("C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d"%(video_number)+"/cropdata/%d.jpg" %(i+1),cv2.IMREAD_COLOR)

    x, y, w,h = data[i][0],data[i][1],data[i][2],data[i][3]
    frameClone = img.copy()
    cv2.rectangle(frameClone,(int(x),int(y)),(int(x+w),int(y+h)),(255,0,0),5)
    cv2.imwrite('C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d'%(video_number)+'/cropdatacheck/%d.jpg' %(i+1), frameClone)


            
# 원본 화면에서 공이 프레임 밖으로 잘리면 안됨!!!!