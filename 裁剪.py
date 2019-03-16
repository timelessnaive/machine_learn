# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 00:21:01 2019

@author: Mr.rice
"""

import cv2 as cv
import os

from retrain_model_classifier import cut

def save(p,path,file):
    if(not os.path.exists(path)):
        os.makedirs(path)
    else:
        if(cv.imwrite(os.path.join(path,file),p)):
            print(os.path.join(path,file))
path=r'C:\code\machine_learn\tfClassifier\image_classification\aim'
for root, dirs, files in os.walk(path):
    for file in files:
        image_path=os.path.join(root,file)
        #try:
        p = cv.imread(image_path)
        p = cut(p)
        save(p, root.replace('aim', 'ori'), file)
        #print(path.replace('aim', 'ori'), file)
        #cv.imwrite(path.replace('aim','ori')+file,p)
        #except:
            #print('error')