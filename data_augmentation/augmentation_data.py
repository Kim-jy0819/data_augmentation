# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:54:14 2021

@author: user
"""

import cv2
import random
import numpy as np
#circle
#from hsv_tracker import HSV_Tracker 
#rectangle
from hsv_tracker2 import HSV_Tracker
import math


class img_aug :
    
    def __init__(self, color_lower, color_upper) :
        
        #indoor lab
        # self.purple_lower = (118, 95, 25)
        # self.purple_upper = (162, 255, 255)
        #outdoor
        # self.purple_lower = (113, 75, 14)
        # self.purple_upper = (173, 255, 255)
        #rooftop
        # self.purple_lower = (110, 80, 20)
        # self.purple_upper = (170, 255, 255)

        self.purple_lower = color_lower
        self.purple_upper = color_upper
        self.x_orig = 1280
        self.y_orig = 720
        self.trial = 0
        self.track = HSV_Tracker(self.y_orig, self.x_orig, self.purple_lower, self.purple_upper) 

        
    def brightness(self, frame) :
        low = 0.4
        high = 1.8
        
        value = random.uniform(low, high)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = np.array(hsv, dtype = np.float64)
        hsv[:,:,1] = hsv[:,:,1]*value
        hsv[:,:,1][hsv[:,:,1]>255]  = 255
        hsv[:,:,2] = hsv[:,:,2]*value 
        hsv[:,:,2][hsv[:,:,2]>255]  = 255
        hsv = np.array(hsv, dtype = np.uint8)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return frame
    
    
    def ch_shift(self, frame) :
        value = 22
        value = random.uniform(-value, value)
        
        frame = frame + value
        frame[:, :, :][frame[:, :, :] > 255] = 255
        frame[:, :, :][frame[:, :, :] < 0] = 0
        frame = frame.astype(np.uint8)
        
        return frame
    
    
    def rotation(self, img,img2) :
        angle = 40
        angle = int(np.random.uniform(-angle, angle))
        
        
        #img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        #img2 = cv2.copyMakeBorder(img2, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        
        h, w = img.shape[: 2]
        
        mean_color=cv2.mean(img)
        
        M = cv2.getRotationMatrix2D((int(w / 2), int(h / 2)), angle, 1)
        img = cv2.warpAffine(img, M, (w, h))
        img2 = cv2.warpAffine(img2, M, (w, h))
        
        img[:,:,0][img[:,:,0]==0]=mean_color[0]
        img[:,:,1][img[:,:,1]==0]=mean_color[1]
        img[:,:,2][img[:,:,2]==0]=mean_color[2]
        
        track2=HSV_Tracker(h, w, self.purple_lower, self.purple_upper)
        mid_x_r, mid_y_r,r_r = track2.hsv_track(img2)        
        
        
      
        

        
        return img, mid_x_r, mid_y_r, r_r#, w_r, h_r
        # return frame, mid_y_r, mid_x_r, r_r
        
    def rotation_rect(self, img,img2) :
       angle = 40
       angle = int(np.random.uniform(-angle, angle))
       
       
       #img = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 0])
       #img2 = cv2.copyMakeBorder(img2, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[0, 0, 0])
       
       h, w = img.shape[: 2]
       
       mean_color=cv2.mean(img)
       
       M = cv2.getRotationMatrix2D((int(w / 2), int(h / 2)), angle, 1)
       img = cv2.warpAffine(img, M, (w, h))
       img2 = cv2.warpAffine(img2, M, (w, h))
       
       img[:,:,0][img[:,:,0]==0]=mean_color[0]
       img[:,:,1][img[:,:,1]==0]=mean_color[1]
       img[:,:,2][img[:,:,2]==0]=mean_color[2]
       
       track3=HSV_Tracker(h, w, self.purple_lower, self.purple_upper)
       x, y,w,h = track3.hsv_track(img2)        
       
       
     
       

       
       return img, x,y,w,h#, w_r, h_r
       # return frame, mid_y_r, mid_x_r, r_r
    def rotation_circ(self, img) :
        angle = 90
        angle = int(random.uniform(-angle, angle))
        
        frame = img.copy()
        
        h, w = frame.shape[: 2]
        
        cross = (h ** 2 + w ** 2) ** 0.5
        alpha = math.atan(720 / 1280)
        beta = math.atan(1280 / 720)
        h_rot = int(cross * math.sin(abs(math.radians(angle)) + alpha))
        
        
        h_add = int((h_rot - h) / 2) + 2
        w_add = int((cross - w) / 2) + 2
        
        frame = cv2.copyMakeBorder(frame, h_add, h_add, w_add, w_add, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        
        h, w = frame.shape[: 2]
        
        
        
        M = cv2.getRotationMatrix2D((int(w / 2), int(h / 2)), angle, 1)
        frame = cv2.warpAffine(frame, M, (w, h))
        
        
        
        # rect_rot = self.track.hsv_track(frame)
        circ_rot = self.track1.hsv_track(frame)
        
        # x_r, y_r, w_r, h_r = rect_rot
        # cv2.rectangle(frame, (x_r, y_r), (x_r + w_r, y_r + h_r), (0, 255, 0), 2)
        # mid_x_r = (x_r + x_r + w_r) / 2
        # mid_y_r = (y_r + y_r + h_r) / 2
        
        x_r, y_r, r_r = circ_rot
        mid_x_r = x_r
        mid_y_r = y_r
        
        y_orig = frame.shape[0]
        x_orig = frame.shape[1]
        
        small_r = min(x_r - r_r, y_r - r_r, x_orig - (x_r +r_r), y_orig - (y_r + r_r))
        large_r = max(x_r - r_r, y_r - r_r, x_orig - (x_r +r_r), y_orig - (y_r + r_r))
        
        rand_size_r = random.randint(2 * int(r_r), 2 * int(r_r) + int(small_r) * 2)
        
        rand_shift_x_r = random.randint(-min(round(mid_x_r) - round(0.5 * rand_size_r), round(0.5 * rand_size_r)) + 2, min(x_orig - round(mid_x_r) + round(0.5 * rand_size_r), round(0.5 * rand_size_r)) - 2)
        rand_shift_y_r = random.randint(-min(round(mid_y_r) - round(0.5 * rand_size_r), round(0.5 * rand_size_r)) + 2, min(y_orig - round(mid_y_r) + round(0.5 * rand_size_r), round(0.5 * rand_size_r)) - 2)
            
        frame = frame[round(mid_y_r) - round(0.5 * rand_size_r) + rand_shift_y_r : round(mid_y_r) + round(0.5 * rand_size_r) + rand_shift_y_r, round(mid_x_r) - round(0.5 * rand_size_r) + rand_shift_x_r : round(mid_x_r) + round(0.5 * rand_size_r) + rand_shift_x_r]
            
        mid_y_r = mid_y_r - (round(mid_y_r) - round(0.5 * rand_size_r) + rand_shift_y_r)
        mid_x_r = mid_x_r - (round(mid_x_r) - round(0.5 * rand_size_r) + rand_shift_x_r)
        
        
        
        
        # return frame, mid_y_r, mid_x_r, w_r, h_r
        return frame, mid_y_r, mid_x_r, r_r