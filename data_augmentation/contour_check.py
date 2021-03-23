# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:49:14 2021

@author: user
"""

import numpy as np
import cv2
import glob

video_number=6
file = 'C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d/datalabeling.csv'%(video_number)
data = np.loadtxt(file, delimiter=',', dtype=np.string_)
data=np.float32(data[:,0:4])
path = glob.glob("C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d"%(video_number)+"/data/*.jpg")

for i in range(len(path)):
    img=cv2.imread("C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d"%(video_number)+"/data/%d.jpg" %(i+1),cv2.IMREAD_COLOR)

    x, y, w, h = data[i][0],data[i][1],data[i][2],data[i][3]
    frameClone = img.copy()
    cv2.rectangle(frameClone,(int(x),int(y)),(int(x+w),int(y+h)),(255,0,0),5)
    cv2.imwrite("C:/Users/charl/Desktop/aims/mester/drone_detection_video/video%d"%(video_number)+"/datacheck/%d.jpg" %(i+1), frameClone)
