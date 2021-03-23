# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:32:37 2020

@author: user
"""

import numpy as np
import cv2
import random
import csv

input = 'C:/Users/charl/Downloads/1.mp4'

cap = cv2.VideoCapture(input)

frame_total = cap.get(cv2.CAP_PROP_FRAME_COUNT)


curr_frame = 0 #영상에서 현재 프레임
frame_skip = 0 # 다음 프레임까지 스킵 수(이건 안건드는게 좋을거에요)
skip_count = 0
frame_idx=1   #데이터프레임 수
quit = 0


while (cap.isOpened() & (curr_frame < frame_total)):
    if quit:
        exit()
        
    while skip_count < frame_skip:
        success, frame = cap.read()
        skip_count = skip_count + 1
        curr_frame = curr_frame + 1
        
    skip_count=0
    success, frame = cap.read()
    
    
    if success == True:
        # Clone frame
        

        frameClone = frame.copy()
        
        curr_frame = curr_frame + 1
        
        cv2.imwrite('C:/Users/charl/Downloads/%d.jpg' %frame_idx, frameClone)
        frame_idx=frame_idx+1