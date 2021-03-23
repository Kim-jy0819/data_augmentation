# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 22:01:23 2021

@author: user
"""

import cv2
import time
import numpy as np

# src = cv2.imread("E:/AIMS/datalabeling/video6/data6/1.jpg", cv2.IMREAD_COLOR)
# src = cv2.circle(src, (424,287) ,51, (145,128,186),-1)
cap = cv2.VideoCapture(1)
ret, src = cap.read()
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
 

def setting_bar():
    cv2.namedWindow('HSV_settings')

    cv2.createTrackbar('H_MAX', 'HSV_settings', 0, 255, lambda x : x)
    cv2.setTrackbarPos('H_MAX', 'HSV_settings', 255)
    cv2.createTrackbar('H_MIN', 'HSV_settings', 0, 255, lambda x : x)
    cv2.setTrackbarPos('H_MIN', 'HSV_settings', 158)
    cv2.createTrackbar('S_MAX', 'HSV_settings', 0, 255, lambda x : x)
    cv2.setTrackbarPos('S_MAX', 'HSV_settings', 163)
    cv2.createTrackbar('S_MIN', 'HSV_settings', 0, 255, lambda x : x)
    cv2.setTrackbarPos('S_MIN', 'HSV_settings', 46)
    cv2.createTrackbar('V_MAX', 'HSV_settings', 0, 255, lambda x : x)
    cv2.setTrackbarPos('V_MAX', 'HSV_settings', 206)
    cv2.createTrackbar('V_MIN', 'HSV_settings', 0, 255, lambda x : x)
    cv2.setTrackbarPos('V_MIN', 'HSV_settings', 124)

setting_bar()


while True:

    ret, src = cap.read()
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    H_MAX = cv2.getTrackbarPos('H_MAX', 'HSV_settings')
    H_MIN = cv2.getTrackbarPos('H_MIN', 'HSV_settings')
    S_MAX = cv2.getTrackbarPos('S_MAX', 'HSV_settings')
    S_MIN = cv2.getTrackbarPos('S_MIN', 'HSV_settings')
    V_MAX = cv2.getTrackbarPos('V_MAX', 'HSV_settings')
    V_MIN = cv2.getTrackbarPos('V_MIN', 'HSV_settings')
    lower = np.array([H_MIN, S_MIN, V_MIN])
    higher = np.array([H_MAX, S_MAX, V_MAX])
    
    Gmask = cv2.inRange(hsv, lower, higher)
    G = cv2.bitwise_and(hsv,hsv,mask= Gmask)
    result=cv2.cvtColor(G,cv2.COLOR_HSV2BGR)
    
    cv2.imshow('cam_load',result)
    cv2.imshow('G',G)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()