# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 19:56:12 2020

@author: user
"""

import numpy as np
import json
#import pandas as pd
import csv

file = 'C:/Users/charl/Desktop/aims/mester/drone_detection_video/video6/via_region_data.json'
f=open(file,'r',encoding='utf-8')
data=json.load(f)

f.close()




label_x=[]
label_y=[]
label_w=[]
label_h=[]
file_name=[]

for i in data.keys():

    if data[i]['regions']=={}:
        continue
    label_x=np.append(label_x,int(data[i]['regions']['0']['shape_attributes']['x']))
    label_y=np.append(label_y,int(data[i]['regions']['0']['shape_attributes']['y']))
    label_w=np.append(label_w,int(data[i]['regions']['0']['shape_attributes']['width']))
    label_h=np.append(label_h,int(data[i]['regions']['0']['shape_attributes']['height']))
    file_name=np.append(file_name, data[i]['filename'])



label=[label_x, label_y, label_w,label_h, file_name]
label=np.transpose(label)

with open('C:/Users/charl/Desktop/aims/mester/drone_detection_video/video6/datalabeling.csv','w',newline='') as f:
    wt=csv.writer(f)
    wt.writerows(label)
    
