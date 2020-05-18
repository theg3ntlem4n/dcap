#!/usr/bin/env python3

import cv2
import time
from display import Display
import numpy as np

W = 1920*2//5
H = 1080*2//5

diff = []

disp = Display(W, H*2)

class FeatureExtractor(object):
    def __init__(self):
        self.orb = cv2.ORB_create(100)
        self.bf = cv2.BFMatcher()
        self.last = None

    def extract(self, img):
        feats = cv2.goodFeaturesToTrack(np.mean(img, axis = 2).astype(np.uint8), 3000, 
            qualityLevel = 0.01, minDistance= 3)
        kps = [cv2.KeyPoint(x=f[0][0], y = f[0][1], _size=20) for f in feats]
        kps, des = self.orb.compute(img, kps)
        
        if self.last is not None:
            matches = self.bf.match(des, self.last['des'])
            #print(matches)        

        self.last = {'kps': kps, 'des':des}

        return feats, kps, des

fe = FeatureExtractor()

def percent_error(feats_original, feats_test):
    original_x = feats_original[0]
    original_y = feats_original[1]

    test_x = feats_test[0]
    test_y = feats_test[1]

    temp_x = abs(test_x - original_x)/original_x
    temp_y = abs(test_y - original_y)/original_y

    mean = np.mean([temp_x, temp_y])
    
    return mean * 100

def process_frame(img_original, img_test):
    accuracy_range = 20

    img_original = cv2.resize(img_original, (W, H))
    img_test = cv2.resize(img_test, (W, H))


    feats_original, kps_original, des_original = fe.extract(img_original)
    feats_test, kps_test, des_test = fe.extract(img_test)

    for p in kps_original:
        u, v = map(lambda x: int(round(x)), p.pt)
        cv2.circle(img_original, (u,v), color = (0,255,0), radius = 3)
    
    for p2 in kps_test:
        a, b = map(lambda y: int(round(y)), p2.pt)
        cv2.circle(img_test, (a, b), color = (0,255,0), radius = 3)

    if len(feats_test) > len(feats_original):
        for x in range(len(feats_original) - 1):
            if abs(feats_original[x][0][0] - feats_test[x][0][0]) < accuracy_range and abs(feats_original[x][0][1] - feats_test[x][0][1]) < accuracy_range: 
                diff.append(percent_error(feats_original[x][0], feats_test[x][0]))
    else:
        for x in range(len(feats_test) - 1):
            if abs(feats_original[x][0][0] - feats_test[x][0][0]) < accuracy_range and abs(feats_original[x][0][1] - feats_test[x][0][1]) < accuracy_range: 
                diff.append(percent_error(feats_original[x][0], feats_test[x][0]))

    disp.paint(img_test, img_original)

cap_original = cv2.VideoCapture("original.mp4")
cap_test = cv2.VideoCapture("test.mp4")

if __name__ == "__main__":

    while cap_original.isOpened() and cap_test.isOpened():
        ret_original, frame_original = cap_original.read()
        ret_test, frame_test = cap_test.read()

        if ret_original == True and ret_test == True:
            process_frame(frame_original, frame_test)
        else:
            print(100 - np.mean(diff))
            break

 
