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
from hsv_tracker import HSV_Tracker
from edge_tracker import EDGE_Tracker
import random
import csv
from augmentation_data import img_aug
import glob





#원본 파일 해상도
x_orig = 1280
y_orig = 720

#각 영상 할때마다 input 주소 바꿔주고, 그에 맞는 purple 범위로 바꿔야 함 
video_number=8
file = 'C:/Users/charl/Desktop/aims/datalabeling/video%d/datalabeling.csv'%video_number
dataset = np.loadtxt(file, delimiter=',', dtype=np.string_)
dataset=np.float32(dataset[:,0:3])

path = glob.glob("C:/Users/charl/Desktop/aims/datalabeling/video%d/data/*.jpg"%video_number)



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

aug_num = 2 # 크롭 당 aug 개수(brightness, ch.shift)
aug_count = 0

aug_rot_num = 3 # 프레임 당 rotate 수
aug_rot_count = 0

curr_frame = 0 #영상에서 현재 프레임
frame_idx = 0 #저장할 크롭 이름, 기본은 0, 이어서 할거면 다음 이름 - 1

norm = 0

label_x = []
label_y = []
# label_w = []
# label_h = []
label_r = []
label_file_name = []



# Read until video is completed
for i in range(len(path)):
    img=cv2.imread("C:/Users/charl/Desktop/aims/datalabeling/video%d"%video_number+"/data/%d.jpg" %(i+1),cv2.IMREAD_COLOR)


    frameClone = img.copy()
    

    ######################################################################
    
    # rect = track2.hsv_track(frameClone)
    # x, y, w, h = rect
    # cv2.rectangle(frameClone, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # mid_x = (x + x + w) / 2
    # mid_y = (y + y + h) / 2
    
    
    x, y, r_r = dataset[i][0],dataset[i][1],dataset[i][2]
    

    mid_x = x
    mid_y = y
    r_r=int(r_r)
    
   
    
   
    
    
    #######################################################################    
    while crop_count < num_of_crops and crop_mode == 1 :
        
        
  
        mid_x = x
        mid_y = y
        r=int(r_r)
        

    
        if r != 0 : 
            norm = 1
        
        
        
        
        
        # mid_x = x
        # mid_y = y
        
        
        
        
        small = min(abs(mid_x - r), abs(mid_y - r), abs(x_orig - (mid_x + r)), abs(y_orig - (mid_y + r)))
        # small = min(r / 2, r * 1.5)
        #large = max(x - r, y - r, x_orig - (x + r), y_orig - (y + r))
        
        
        
       
        rand_size = random.randint(int(r)+int(small/2), int(r) + int(small))
    
    
    
        #rand_shift_x = random.randint(-min(round(mid_x) - round(rand_size), round(rand_size)) + 2, min(x_orig - round(mid_x) + round(rand_size), round(rand_size)) - 2)
        #rand_shift_y = random.randint(-min(round(mid_y) - round(rand_size), round(rand_size)) + 2, min(y_orig - round(mid_y) + round(rand_size), round(rand_size)) - 2)
        
        rand_shift_x=random.randint(1,int(small/2+r/5))
        rand_shift_y=random.randint(1,int(small/2+r/5))
        
        crop = frameClone[round(mid_y) - round(rand_size) + rand_shift_y : round(mid_y) + round(rand_size) + rand_shift_y, round(mid_x) - round(rand_size) + rand_shift_x : round(mid_x) + round(rand_size) + rand_shift_x]
        
        mid_y = mid_y - (round(mid_y) - round(rand_size) + rand_shift_y)
        mid_x = mid_x - (round(mid_x) - round(rand_size) + rand_shift_x)

        
        crop2=crop.copy()
        cropclone=crop.copy()
        crop2 = cv2.circle(crop2, (int(mid_x),int(mid_y)),int(r) , (145,128,186),-1)
        
        
       
        
      
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
            r = r * trans
            
            
            
            cv2.imwrite('C:/Users/charl/Desktop/aims/datalabeling/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, crop)
            label_x = np.append(label_x, mid_x)
            label_y = np.append(label_y, mid_y)
            # label_w = np.append(label_w, w)
            # label_h = np.append(label_h, h)
            label_r = np.append(label_r, r)
            label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
            
            
            while aug_count < aug_num :
                aug1 = aug.brightness(crop)
                frame_idx = frame_idx + 1
                cv2.imwrite('C:/Users/charl/Desktop/aims/datalabeling/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, aug1)
                label_x = np.append(label_x, mid_x)
                label_y = np.append(label_y, mid_y)
                # label_w = np.append(label_w, w)
                # label_h = np.append(label_h, h)
                label_r = np.append(label_r, r)
                label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
                
                
                aug2 = aug.ch_shift(crop)
                frame_idx = frame_idx + 1
                cv2.imwrite('C:/Users/charl/Desktop/aims/datalabeling/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, aug2)
                label_x = np.append(label_x, mid_x)
                label_y = np.append(label_y, mid_y)
                # label_w = np.append(label_w, w)
                # label_h = np.append(label_h, h)
                label_r = np.append(label_r, r)
                label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
                
                aug_count = aug_count + 1
                
            aug_count = 0
            
            
            while aug_rot_count < aug_rot_num : 
                
                # aug3, mid_y_r, mid_x_r, w_r, h_r = aug.rotation(frame)
                #frameClone: 원본 frameClone2: circle 그린 사본 -> hsv_tracker2를 활용할 수 있음.
                aug3, mid_x_r, mid_y_r, r_rr = aug.rotation(cropclone,crop2)
                # aug3, mid_y_r, mid_x_r, r_r = aug.rotation_circ(frame)
                
                trans_r = 400 / aug3.shape[0]
                
                if aug3.shape[0] == aug3.shape[1]:
                    
                    frame_idx = frame_idx + 1
                    
                    aug3 = cv2.resize(aug3, dsize=(400, 400), interpolation=cv2.INTER_AREA)
                    mid_x_r = mid_x_r * trans_r
                    mid_y_r = mid_y_r * trans_r
                    # w_r = w_r * trans_r
                    # h_r = h_r * trans_r
                    r_rr = r_rr * trans_r
                
                    cv2.imwrite('C:/Users/charl/Desktop/aims/datalabeling/video%d'%video_number+'/cropdata/%d.jpg' %frame_idx, aug3)
                
                #x, y, diameter 저장
                    label_x = np.append(label_x, mid_x_r)
                    label_y = np.append(label_y, mid_y_r)
                    # label_w = np.append(label_w, w_r)
                    # label_h = np.append(label_h, h_r)
                    label_r = np.append(label_r, r_rr)
                    label_file_name = np.append(label_file_name, '%d.jpg' %frame_idx)
                    
                    aug_rot_count = aug_rot_count + 1
                
                
            aug_rot_count = 0    
      
        crop_count = crop_count + 1
       
    if crop_count == num_of_crops:
        crop_count = 0
        skip_count = 0
        norm = 0
   

# data = [label_x, label_y, label_w, label_h, label_file_name]
data = [label_x, label_y, label_r, label_file_name]
data = np.transpose(data)
with open('C:/Users/charl/Desktop/aims/datalabeling/video%d'%video_number+'/cropdata.csv', 'w', newline = '') as f:
    wt = csv.writer(f)
    wt.writerows(data)


# contour checking
file = 'C:/Users/charl/Desktop/aims/datalabeling/video%d/cropdata.csv'%(video_number)
data = np.loadtxt(file, delimiter=',', dtype=np.string_)
data=np.float32(data[:,0:3])
path = glob.glob("C:/Users/charl/Desktop/aims/datalabeling/video%d"%(video_number)+"/cropdata/*.jpg")

for i in range(len(path)):
    img=cv2.imread("C:/Users/charl/Desktop/aims/datalabeling/video%d"%(video_number)+"/cropdata/%d.jpg" %(i+1),cv2.IMREAD_COLOR)

    x, y, r_r = data[i][0],data[i][1],data[i][2]
    frameClone = img.copy()
    cv2.circle(frameClone,(int(x),int(y)),int(r_r),(255,0,0),5)
    cv2.imwrite('C:/Users/charl/Desktop/aims/datalabeling/video%d'%(video_number)+'/cropdatacheck/%d.jpg' %(i+1), frameClone)


            
# 원본 화면에서 공이 프레임 밖으로 잘리면 안됨!!!!