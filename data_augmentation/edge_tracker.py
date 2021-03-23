# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:42:11 2020

@author: Donghee Lee
"""

import cv2
import numpy as np


class EDGE_Tracker:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.diameter = 0
        # self.minRadius = 0
        # self.maxRadius = 0
        
        
        
    def edge_track(self, img, minRad, maxRad):
        # self.minRadius = minRad
        # self.maxRadius = maxRad
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)
        # img = cv2.GaussianBlur(img, (21,21), 0)
        img = cv2.bilateralFilter(img, 7, 50, 50)
        #40/24 for tello_vid
        
        
        #gaussian blur 했을 때는 param1 = 40 , param2 = 30
        #bilateral filter 했을 때는 param1 = 40, param2 = 45
        all_circs = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 150, param1=45, param2=40, minRadius = minRad, maxRadius = maxRad)
        # all_circs_rounded = np.uint16(np.around(all_circs))
        
        # if all_circs_rounded.shape[1] == 1:
        #     self.x = all_circs_rounded[0, 0, 0]
        #     self.y = all_circs_rounded[0, 0, 1]
        #     self.diameter = all_circs_rounded[0, 0, 2]
            
        
        
        if all_circs is not None:    
            if all_circs.shape[1] == 1:
                self.x = all_circs[0, 0, 0]
                self.y = all_circs[0, 0, 1]
                self.diameter = all_circs[0, 0, 2]
                
                for i in all_circs[0, :]:
                    cv2.circle(img, (i[0], i[1]), i[2], (50, 200 , 200), 5)
                    cv2.circle(img, (i[0], i[1]), 2, (255,0,0), 3)    
        
        else:
            self.x = 0
            self.y = 0
            self.diameter = 0
            
        return all_circs, self.x, self.y, self.diameter
    
            
        
        # count = 1
        # for i in all_circs_rounded[0, :]:
        #     cv2.circle(img, (i[0], i[1]), i[2], (50, 200 , 200), 5)
        #     cv2.circle(img, (i[0], i[1]), 2, (255,0,0), 3)
            # cv2.putText(img, 'ball ' + str(count), (i[0]-70, i[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255,0,0), 2)
            # count +=1